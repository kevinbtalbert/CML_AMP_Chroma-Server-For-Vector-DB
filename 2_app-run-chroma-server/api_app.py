from typing import Any, Union, Optional
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import os
import threading
import asyncio
import subprocess
import uvicorn
from typing import Any, Union, Optional
import chromadb
from chromadb.utils import embedding_functions

EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

print("initialising Chroma DB connection...")
chroma_client = chromadb.PersistentClient()
print("Chroma DB initialised")

print(f"Getting '{COLLECTION_NAME}' as object...")
if chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=EMBEDDING_FUNCTION):
    print("Success")
    collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=EMBEDDING_FUNCTION)
else:
    print("Creating new collection...")
    collection = chroma_client.create_collection(name=COLLECTION_NAME, embedding_function=EMBEDDING_FUNCTION)
    print("Success")

# Get latest statistics from index
current_collection_stats = collection.count()
print('Total number of embeddings in Chroma DB index is {}.'.format(current_collection_stats.get('total_vector_count')))

app = FastAPI()

# Helper function for generating responses for the Chroma DB
def get_responses(question, max_results):
    results = collection.query(query_texts=question, n_results=max_results) 
    print(results)
    # Return text of the nearest knowledge base chunk(s)
    #response = load_context_chunk_from_data(matching_files[0])
    
    return results


# Helper function for adding documents to the Chroma DB
def upsert_document(document, metadata=None, classification="public", file_path=None):
    
    # Push document to Chroma vector db
    if file_path is not None:
        response = collection.add(
            documents=[document],
            metadatas=[{"classification": classification}],
            ids=[file_path]
        )
    else:
        response = collection.add(
            documents=[document],
            metadatas=[{"classification": classification}],
            ids=mystring[:50]
        )
    return response

# Return the Knowledge Base doc based on Knowledge Base ID (relative file path)
def load_context_chunk_from_data(id_path):
    with open(id_path, "r") as f: # Open file in read mode
        return f.read()

@app.get("/")
def status_gpu_check() -> dict[str, str]:
    chroma_status = "Chroma Vector DB READY" if collection else "Unavailable"
    return {
        "server_status": "Web server is ALIVE",
        "chroma_status": chroma_status
    }

# This defines the data json format expected for the endpoint, change as needed
class TextInput(BaseModel):
    inputs: str
    parameters: Union[dict[str, Any], None]

@app.post("/upsert")
def upsert_endpoint(data: TextInput) -> dict[str, str]:
    try:
        document = data.inputs
        params = data.parameters or {}
        print(str(document))
        
        if 'metadata' in params:
            metadata = int(params['metadata'])
            print("Using: "+ str(metadata))
        else:
            metadata = None
            
        if 'classification' in params:
            classification = int(params['classification'])
        else:
            classification = "public"
        
        if 'file_path' in params:
            file_path = int(params['file_path'])
            print("Using: "+ str(file_path))
        else:
            file_path = None

        print("Using: "+ str(classification))
            
        res = upsert_document(document, metadata, classification, file_path)

        return {"response": res}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_endpoint(data: TextInput) -> dict[str, str]:
    try:
        question = data.inputs
        params = data.parameters or {}
        
        if 'max_results' in params:
            max_results = int(params['max_results'])
        else:
            max_results = 1
            
        res = get_responses(question, max_results)
        return {"response": res}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ['CDSW_APP_PORT']), log_level="warning", reload=False)

server_thread = threading.Thread(target=run_server)
server_thread.start()