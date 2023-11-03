from typing import Any, Union, Optional
from fastapi import FastAPI
from fastapi import HTTPException
import os
import threading
import asyncio
import subprocess
from typing import Any, Union, Optional
from sentence_transformers import SentenceTransformer ## Needed??
import chromadb
from chromadb.utils import embedding_functions

EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

print("initialising Chroma DB connection...")
chroma_client = chromadb.Client()
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
def get_responses(question):
    
    # Get nearest knowledge base chunk for a user question from a vector db
    response = get_nearest_chunk_from_chroma_vectordb(index, question)
    
    return response

# Helper function for adding documents to the Chroma DB
def upsert_document(collection, document, metadata, classification):
    
    # Get nearest knowledge base chunk for a user question from a vector db
    response = upsert_to_chroma_vectordb(index, question)
    
    return response

# Get embeddings for a user question and query Pinecone vector DB for nearest knowledge base chunk
def get_nearest_chunk_from_chroma_vectordb(index, question):
    # Generate embedding for user question with embedding model
    retriever = SentenceTransformer(EMBEDDING_MODEL_REPO)
    xq = retriever.encode([question]).tolist()
    xc = index.query(xq, top_k=5,
                 include_metadata=True)
    
    matching_files = []
    for match in xc['matches']:
        # extract the 'file_path' within 'metadata'
        file_path = match['metadata']['file_path']
        matching_files.append(file_path)

    # Return text of the nearest knowledge base chunk 
    # Note that this ONLY uses the first matching document for semantic search. matching_files holds the top results so you can increase this if desired.
    response = load_context_chunk_from_data(matching_files[0])
    return response
  
# Return the Knowledge Base doc based on Knowledge Base ID (relative file path)
def load_context_chunk_from_data(id_path):
    with open(id_path, "r") as f: # Open file in read mode
        return f.read()

# Get embeddings for a user question and query Chroma vector DB for nearest knowledge base chunk
def get_nearest_chunk_from_chroma_vectordb(collection, document, metadata, classification):
    
    
    return "Successful upload"
    
    
    
@app.get("/")
def status_gpu_check() -> dict[str, str]:
    gpu_msg = "Available" if tf.test.is_gpu_available() else "Unavailable"
    return {
        "status": "I am ALIVE!",
        "gpu": gpu_msg
    }

@app.post("/upsert")
def upsert_endpoint(data: TextInput) -> dict[str, str]:
    try:
        question = data.inputs
        params = data.parameters or {}
        
        if 'metadata' in params:
            metadata = int(params['metadata'])
            
        if 'classification' in params:
            classification = int(params['classification'])
            
        print(str(question))
        print("Using: "+ str(metadata))
        print("Using: "+ str(classification))
            
        res = upsert_document(collection, document, metadata, classification)

        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate_endpoint(data: TextInput) -> dict[str, str]:
    try:
        question = data.inputs
        res = get_responses(question)
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ['CDSW_APP_PORT']), log_level="warning", reload=False)

server_thread = threading.Thread(target=run_server)
server_thread.start()