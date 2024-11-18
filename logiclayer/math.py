import datalayer.math_data as math_data


def GetMathData(quert_text):
    results = math_data.QueryData(quert_text)
    resultsToDisplay = []
    # Print the results
    for match in results["matches"]:
        #resultsToDisplay.append(f"ID: {match['id']}, Score: {match['score']}, title: {match['metadata']['title']}, link: {match['metadata']['link']}, imagelink: {match['metadata']['imagelink']}, comment: {match['metadata']['comment']}, created_at: {match['metadata']['created_at']}")        
        resultsToDisplay.append(f"ID: {match['id']}, Score: {match['score']}, value: {match['metadata']['p_value']}")

    return resultsToDisplay

def CreateMathData():
    data = math_data.ReadDataFromLocalFolder()    
    dataEmbedding = math_data.DataToEmbedding(data)
    results = math_data.UpsertData(dataEmbedding)

    if results:
        return {"message": "Create/Update Math Data successfully"}
    else:
        return {"message": "Create/Update Math Data failed"}