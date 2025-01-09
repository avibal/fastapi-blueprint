
import os
import google.generativeai as genai
import json

# **Set the API_KEY environment variable before code execution**
os.environ["API_KEY"] = "*********"  # Replace with your actual key

# Configure genai with the API key from the environment variable
genai.configure(api_key=os.environ["API_KEY"])




def GetDataByInput(input):
    model = genai.GenerativeModel('gemini-1.5-pro-001')

    # Use the model for text generation (replace with your desired prompt)
    #"פרט לי את שלבי הפתרון לתרגיל שורש ריבועי של 11"
    prompt =  input 
    response = model.generate_content(prompt)

    text_response = response.text

    # 1. Split into paragraphs
    paragraphs = text_response.split("\n\n")

    # 2. Create a list to store the formatted paragraphs
    formatted_paragraphs = []

    # 3. Iterate through each paragraph and format it
    for index,paragraph in enumerate(paragraphs):
        # 3.1. Remove bold formatting
        paragraph = paragraph.replace("**", "")

        # 3.2. Replace newline characters with HTML line breaks
        paragraph = paragraph.replace("\n", "")

        # 3.3. Add the formatted paragraph to the list        
        formatted_paragraphs.append({"step_number" + str(index + 1):  paragraph}) 

    # 4. Create the final JSON data
    json_data = {"steps": formatted_paragraphs}
    return json_data

def GetMockData():

    text_response = "אין צורך בשלבי פתרון מורכבים עבור מציאת השורש הריבועי של 44, מכיוון שמדובר בידיעה בסיסית בטבלאות הכפל. \n\n**השורש הריבועי של 4 הוא 2.** \n\nזאת מכיוון ש: 2 * 2 = 4. \n\n**הסבר כללי על שורש ריבועי:**\n\nשורש ריבועי של מספר הוא המספר שכאשר מכפילים אותו בעצמו, התוצאה היא המספר המקורי. \n"

    # 1. Split into paragraphs
    paragraphs = text_response.split("\n\n")

    # 2. Create a list to store the formatted paragraphs
    formatted_paragraphs = []

    # 3. Iterate through each paragraph and format it
    for index,paragraph in enumerate(paragraphs):
        # 3.1. Remove bold formatting
        paragraph = paragraph.replace("**", "")

        # 3.2. Replace newline characters with HTML line breaks
        paragraph = paragraph.replace("\n", "")

        # 3.3. Add the formatted paragraph to the list        
        formatted_paragraphs.append({"step_number" + str(index + 1):  paragraph}) 

    # 4. Create the final JSON data
    json_data = {"steps": formatted_paragraphs}
    return json_data

