import chromadb
import os 
import json
import dotenv
import chromadb.utils.embedding_functions as embedding_functions
dotenv.load_dotenv()

huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=os.environ.get("HUGGINGFACE_API_KEY"),
    model_name="BAAI/bge-small-en-v1.5"
)

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
            embeddings = huggingface_ef([str(song)])
            db(str(song), embeddings[0][0], str(data.index(song)))

def query_search(song, n=3):
    embedding=huggingface_ef([song])
    res=collection.query(
        query_embeddings=[embedding[0][0]],
        n_results=n,
    )

    return res["documents"]

embed()