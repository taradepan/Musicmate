import chromadb
import os 
import json
import dotenv
import google.generativeai as genai
import chromadb.utils.embedding_functions as embedding_functions
dotenv.load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY')) 

  
google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=os.environ.get("GOOGLE_API_KEY"))    
client = chromadb.Client()
collection = client.get_or_create_collection(name="main")

def db(text, embed, ids):
    collection.add(
    documents=[text],
    embeddings=[embed],
    ids=[ids]
    )
    print(text + " added to database")

def embed():
    with open('data.json', 'r') as f:
        data = json.load(f)
        data = data["songs"]
        for song in data:
            embeddings = google_ef([str(song)])
            db(str(song), embeddings[0][0], str(data.index(song)))

def query_search(song):
    embedding=google_ef([song])
    res=collection.query(
        query_embeddings=[embedding[0][0]],
        n_results=3,
    )

    return res["documents"]

embed()