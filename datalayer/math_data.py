
from langchain_openai.embeddings import OpenAIEmbeddings
from transformers import pipeline
import torch
import json 
import requests
from pinecone import Pinecone,ServerlessSpec
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lxml import etree
from sympy import sympify
from sympy.printing.latex import latex
from transformers import AutoModel, AutoTokenizer
import latex2mathml.converter
from docxlatex import Document

# Initialize the tokenizer and model
model_name = "tbs17/MathBERT"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load the model with hidden states output
model = AutoModel.from_pretrained(model_name, output_hidden_states=True)



index_name = "mathdata"
ns1 = "mathdata"
modelDimention = 50
pc = None
PinCone_api_key="396a6bab-9a8e-4388-8bfe-bc28dab99239"
OpenAI_api_key="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"
#embeddings = OpenAIEmbeddings(openai_api_key=OpenAI_api_key)
#model = SentenceTransformer('all-MiniLM-L6-v2')


json_file_path= './datalayer/recipes.json'
#model = SentenceTransformer('mathbert/mathbert-base-cased')

#model = SentenceTransformer('allenai/scibert_scivocab_uncased')


def CheckIndexExists():    
    pc = Pinecone(api_key=PinCone_api_key)
    try:
        pc.describe_index(name=index_name)
        return True
    except Exception:
        return False

def CreateIndex():
   pc = Pinecone(api_key=PinCone_api_key)
   pc.create_index(
    name=index_name,
    dimension=modelDimention, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

def UpsertData(vectorsData):
    
    pc = Pinecone(api_key=PinCone_api_key)
    if not CheckIndexExists():    
        CreateIndex()

    index = pc.Index(index_name)    
    UpsertResponse = index.upsert(vectors=vectorsData, namespace=ns1)        
    return UpsertResponse
   


def VectorizeData(data):

    inputs = tokenizer(data, return_tensors="pt", truncation=True, padding=True)
        # 2. Get the model output (hidden states)
    model.eval()

    with torch.no_grad():
        # Get the model outputs
        outputs = model(**inputs)

        # Extract the last hidden state
        last_hidden_state = outputs.hidden_states[-1]

    # 3. Option A: Mean Pooling (for sentence-level embeddings)
    embeddings = last_hidden_state.mean(dim=1)

    vector = embeddings.tolist()  
    #vector = vector[:modelDimention]     
    vector = [float(v) for v in vector[0][:modelDimention]]

    return vector

def QueryData(quert_text):
    
    pc = Pinecone(api_key=PinCone_api_key)    
    index = pc.Index(index_name)

    vector =  VectorizeData(quert_text)

    # Perform a search in Pinecone
    results = index.query(
        namespace=ns1,
        vector=vector,
        top_k=10,  # Retrieve top 10 most similar recipes
        include_values=True,
        include_metadata=True
    )
    
    # Print results
    print(','.join(str(item) for item in vector))

    return results


# Clean up
def delete_index(index_name):    
    pc.delete_index(index_name)


def DataToEmbedding(data):
   
    # Initialize an empty list to store vectors
    vectors = []  

    #vectors = embeddings.embed_documents([p.text for p in data])

    # Upsert data into Pinecone
    for i, text in enumerate(data):        
        vector = VectorizeData(text)
        
        vectors.append(
                {
                    "id": f"p_{i}",
                    "values": vector,
                    "metadata": {"p_value": data[i]}
                }
            )            
        
    return vectors

def ReadDataFromLocalFolder():



    # Path to your local Word document
    docx_path = r'C:\AB\Dev\MyMatcon\MathData\A571_1.docx'

    xslt_path = r'C:\AB\Dev\MyMatcon\MathData\omml2mml.xsl'        # Replace with the path to the XSLT file

    # Create a Document object with the path to your .docx file
    doc = Document(docx_path)

    # Extract the text, including LaTeX equations
    text = doc.get_text()
    
    lines = text.splitlines()
    lines1 = [line.replace('$','') for line in lines]    
    lines2 = [line.replace('$$','') for line in lines1]    
    lines3 = [line.replace('frac','') for line in lines2]
    lines4 = [line.replace('\\','') for line in lines3]    
    cleaned_lines = [line.strip() for line in lines4 if line.strip()]    


    data = []
    for i, paragraph in enumerate(cleaned_lines):
        if "IMAGE#" not in paragraph:  # Check if "Image" is NOT in the paragraph
            data.append(paragraph)      

    return data




def ReadDataFromGdrive():

    """
    Downloads a file from Google Drive using the file ID.
    
    :param file_id: str, Google Drive file ID
    :param destination: str, path to save the downloaded file
    """
    # URL to fetch the file from Google Drive
    URL = "https://docs.google.com/document/d/1UCdTiksceD8qhan0oBZUJDElBFWG1po6"

    # Replace 'FILE_ID' with the actual file ID from your Google Drive link
    file_id = "1UCdTiksceD8qhan0oBZUJDElBFWG1po6"  # Extracted from the shareable link
    destination = "downloaded_file.docx"  # Path to save the file locally

    # Make the request
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    
    
    # Check if the response is OK
    if response.status_code == 200:
        # Save the file to the destination
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

    doc = Document(destination)

    # Print the content of the document
    for paragraph in doc.paragraphs:
        print(paragraph.text)

    
    data = doc.paragraphs

    return data



def ConvertToTextArray(data):
    # Extract text and other keys
    dataAsJSON = [
        {
            "title": item['title'] if 'title' in item else '',
            "link": item['link'] if 'link' in item else '',
            "imagelink": item['imagelink'] if 'imagelink' in item else '',
            "comment": item['comment'] if 'comment' in item else '',
            "created_at": item['created_at'] if 'created_at' in item else ''        
        }
        for item in data
    ]    
    return dataAsJSON