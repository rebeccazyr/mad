from sentence_transformers import SentenceTransformer, models
from transformers import AutoModel, AutoTokenizer

model_path = "./saved_model"

word_embedding_model = models.Transformer(model_path)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
model.save("./converted_model")