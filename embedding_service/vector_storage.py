import itertools
import logging
import pinecone

logger = logging.getLogger(__name__)

class VectorStorage:
    """Class for interacting with vector storage"""
    
    def __init__(self, api_key: str, api_env: str, index_dimension: int, **kwargs):
        """Initialize the vector storage"""
        self._setup_vector_storage(**kwargs)
        self._index = None
        self._index_name = kwargs.get("index_name", "index")

    def _setup_vector_storage(self, api_key: str, api_env: str, index_dimension: int, index_name="index", metric="cosine"):
        """Setup the vector storage"""
        pinecone.init(api_key=api_key, environment=api_env)
        
        if index_name in pinecone.list_indexes():
            logger.info(f"Index {index_name} already exists, connecting to existing index")
        else:
            pinecone.create_index(name=index_name, dimension=index_dimension, metric=metric)

        self._index = pinecone.Index(name=index_name)


    def upload(self, vectors: list):
        """Upload vectors to the vector storage"""        
        with pinecone.Index(name=self._index_name, pool_threads=30) as index:
            async_results = [
                index.upsert(vectors=vectors_chunk, async_req=True)
                for vectors_chunk in self._chunk(vectors)
            ]
            # Wait for the async requests to finish in case of error
            [async_result.get() for async_result in async_results]


    def query(self, vector: list, top_k: int = 5, **kwargs):
        """Query the vector storage
        Args:
            vector: The vector to query
            top_k: The number of results to return
            filters: filters object
            include_values: Whether to include the values in the response
            include_metadata: Whether to include the metadata in the response
        
        """
        return self._index.query(queries=vector, top_k=top_k, **kwargs)


    def _chunk(self, iterable, batch_size=100):
        """Yield successive n-sized chunks from lst."""
        it = iter(iterable)
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, batch_size))
