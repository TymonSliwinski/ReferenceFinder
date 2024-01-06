from flask import Flask
from markupsafe import escape
from vector_storage import VectorStorage
from constants import PINECONE_API_KEY, PINECONE_ENVIRONMENT

app = Flask(__name__)

vector_storage = VectorStorage(
    api_key=PINECONE_API_KEY,
    api_env=PINECONE_ENVIRONMENT,
    index_dimension=1536,
)

@app.route('/api/embed')
def embed(text: str):
    return text

@app.route('/api/vectors/query')
def query(vector: list, top_k: int = 5, **kwargs):
    vector_storage.query(escape(vector), top_k, **kwargs)
