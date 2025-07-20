import torch
from sentence_transformers import SentenceTransformer


class SentenceEncoder(torch.nn.Module):
    """
    Wrapper for SentenceTransformer model to encode input texts.
    """

    def __init__(self, model_name="BAAI/bge-base-en-v1.5"):
        super().__init__()
        self.model = SentenceTransformer(model_name)

    def forward(self, texts):
        """
        Encode a list of input texts into dense embeddings.
        """
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        return embeddings
