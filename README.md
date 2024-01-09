# RefenceFinder
## Description
ReferenceFinder is an app that provides an easy way to find references for your next science paper, based on PDF files provided by you.  
  
To allow for semantic search across multiple text sources, the application leverages text-to-vector embedding using pre-trained BERT-based model and Pinecone vector database.

## Project setup
### Environmental variables
Create `.env` file in the project root
```.env
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
```
### Installation
1. create venv using `$ python -m venv .venv`
1.1 `$ source .venv/bin/activate`
2. run `$ pip install -r requirements.txt`

### Running the server
Start the flask server
`python app/app.py`

### Run with Docker
`$ docker build -t <tag> . && docker run --env-file .env -p 5000:5000 <tag>`

## Usage
After spinning up the server, place all PDFs you need in a directory (e.g. *data*) and run `$ python scripts/process_files.py path/to/pdfs`. This will loads all your PDF files, embed chunks and insert into Pinecone database

### API Documentation
<details>
<summary><strong><code>POST /api/embed</code></strong></summary>

<br/>

Embed text to vector.

**Headers**
```
Content-Type: application/json
```

**Body**
```json
{
    "text": "Text to embed."
}
```

**Response**
```
[-0.03076675347983837,-0.040745943784713745,-0.060128629207611084,...]
```

</details>

<details>
<summary><strong><code>POST /api/vectors/upload</code></strong></summary>

<br/>

Upload vector to the database.

**Headers**
```
Content-Type: application/json
```

**Body**
```json
{
    "vectors": [
        {
            "id": "vec-id",
            "values": [-0.03076682984828949,-0.06012870371341705,...], // n-dim vector
            "metadata": {
                "text": "Embedded text"
            }
        }
    ]
}
```

**Response**
```json
{
    "message": "Success"
}
```

</details>

<details>
<summary><strong><code>POST /api/vectors/query</code></strong></summary>

<br/>

Query the database against text.

**Headers**
```
Content-Type: application/json
```

**Body**
```json
{
    "text": "Text to search",
    "top_k": 5, // number of results
    "filers": {
        "key": "value"
    },
    "include_values": false,
    "include_metadata": true
}
```

**Response**
```json
{
    "matches": [
        {
            "id": "vec-id",
            "metadata": {
                "file": "file-name",
                "page": 4.0,
                "text": "Text that is similar to provided query."
            },
            "score": 0.841730183,
            "values": []
        },
        ... // other matches
    ]
}
```

</details>