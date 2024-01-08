from flask import Flask, request
from markupsafe import escape
from embeddings import Embeddings
from vector_storage import VectorStorage
from constants import PINECONE_API_KEY, PINECONE_ENVIRONMENT

app = Flask(__name__)


embeddings = Embeddings()

vector_storage = VectorStorage(
    api_key=PINECONE_API_KEY,
    api_env=PINECONE_ENVIRONMENT,
    index_dimension=embeddings.dimension,
)

@app.route('/api/embed', methods=['POST'])
def embed():
    text = request.json.get('text')
    vector = embeddings.embed(text)
    return vector

@app.route('/api/vectors/upload', methods=['POST'])
def upload():
    vectors = request.json.get('vectors')
    vector_storage.upload(vectors)
    return { 'message': 'Success' }

@app.route('/api/vectors/query')
def query(vector: list, top_k: int = 5, **kwargs):
    return vector_storage.query(escape(vector), top_k, **kwargs)


if __name__ == '__main__':
    app.run()
