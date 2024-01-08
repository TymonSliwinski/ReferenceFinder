import torch
from sentence_transformers import SentenceTransformer

class Embeddings:
    _device = 'cuda' if torch.cuda.is_available() else 'cpu'
    _model = SentenceTransformer('all-MiniLM-L6-v2', device=_device)
    dimension = _model.get_sentence_embedding_dimension()
    
    def __init__(self):
        pass

    def embed(self, text: str) -> list[float]:
        return self._model.encode(text).tolist()
