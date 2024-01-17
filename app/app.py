import argparse
from flask import Flask, render_template, request, Request
from markupsafe import escape
from embeddings import Embeddings
from vector_storage import VectorStorage
from constants import PINECONE_API_KEY, PINECONE_ENVIRONMENT

embeddings = Embeddings()

vector_storage = VectorStorage(
    api_key=PINECONE_API_KEY,
    api_env=PINECONE_ENVIRONMENT,
    index_dimension=embeddings.dimension,
)

def query_logic(request: Request):
    text: str = request.json.get('text')
    if not text:
        return { 'message': 'Missing query text' }, 400

    vector = embeddings.embed(str(escape(text)))
    top_k: int = int(request.json.get('top_k', 5))
    args = dict(
        filters = request.json.get('filters', {}),
        include_values = request.json.get('include_values', False),
        include_metadata = request.json.get('include_metadata', True),
    )
    results = vector_storage.query(vector, top_k=top_k, **args)
    for vector in results.get('matches', []):
        if vector.get('metadata', {}).get('page'):
            vector['metadata']['page'] = int(vector['metadata']['page'])
    return results.to_dict()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vectors/query', methods=['POST'])
def query_page():
    results = query_logic(request)
    if isinstance(results, tuple):
        return results

    return render_template('results.html', results=results['matches'])

@app.route('/api/embed', methods=['POST'])
def embed():
    text = request.json.get('text')
    if not text:
        return { 'message': 'Missing text' }, 400
    vector = embeddings.embed(escape(text))
    return vector

@app.route('/api/vectors/upload', methods=['POST'])
def upload():
    vectors = request.json.get('vectors')
    if not vectors:
        return { 'message': 'Missing vectors' }, 400
    try:
        vectors = [dict(
            id = escape(vector['id']),
            values = escape(vector['values']),
            metadata = escape(vector['metadata']),
        ) for vector in vectors]
        vector_storage.upload(vectors)
    except Exception as e:
        return { 'message': str(e) }, 400
    return { 'message': 'Success' }

@app.route('/api/vectors/query', methods=['POST'])
def query():
    return query_logic(request)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()
