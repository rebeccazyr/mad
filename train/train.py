import os
import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, models
from dataset import TripletContrastiveDataset
from loss import batched_multi_positive_contrastive_loss
from tqdm import tqdm

os.environ["CUDA_VISIBLE_DEVICES"] = "4"

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")
if device.type == "cuda":
    print(f"CUDA device index: {torch.cuda.current_device()}")
    print(f"CUDA device name: {torch.cuda.get_device_name(device)}")
# Load SentenceTransformer model
torch.cuda.empty_cache()
model_name = "BAAI/bge-base-en-v1.5"
word_embedding_model = models.Transformer(model_name)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
model.to(device)

# Load dataset
dataset = TripletContrastiveDataset(
    claim_to_evidences_path="./data/train_set.json",
    evidence_id_to_sentence_path="./data/evidence_id_to_text.json",
    claim_id_to_claim_path="./data/example_to_claim.json"
)

# Collate function for batching
def collate_fn(batch):
    claim_texts = []
    pos_sentences_batch = []
    neg_sentences_batch = []

    for claim_text, pos_sentences, neg_sentences in batch:
        claim_texts.append(claim_text)
        pos_sentences_batch.append(pos_sentences)
        neg_sentences_batch.append(neg_sentences)

    return claim_texts, pos_sentences_batch, neg_sentences_batch

# DataLoader
dataloader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)

# Optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

# Training loop
model.train()
for epoch in range(3):
    total_loss = 0.0
    for claim_texts, pos_sentences_batch, neg_sentences_batch in tqdm(dataloader, desc=f"Epoch {epoch+1}"):
        optimizer.zero_grad()

        # Flatten positive and negative sentences
        flat_pos = [s for group in pos_sentences_batch for s in group]
        flat_neg = [s for group in neg_sentences_batch for s in group]

        # Tokenize & encode via forward pass
        def encode_texts(texts):
            features = model.tokenize(texts)
            for key in features:
                features[key] = features[key].to(device)
            with torch.set_grad_enabled(True):
                return model.forward(features)["sentence_embedding"]

        h_i = encode_texts(claim_texts)
        h_pos = encode_texts(flat_pos)
        h_neg = encode_texts(flat_neg)

        # Split back into positives_list / negatives_list
        positives_list = []
        negatives_list = []

        pos_idx = 0
        for group in pos_sentences_batch:
            count = len(group)
            positives_list.append(h_pos[pos_idx:pos_idx + count])
            pos_idx += count

        neg_idx = 0
        for group in neg_sentences_batch:
            count = len(group)
            negatives_list.append(h_neg[neg_idx:neg_idx + count])
            neg_idx += count

        # Compute loss
        loss = batched_multi_positive_contrastive_loss(h_i, positives_list, negatives_list)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} - Loss: {total_loss / len(dataloader):.4f}")

# Save model
save_path = "./saved_model_new"
os.makedirs(save_path, exist_ok=True)
model.save(save_path)
print(f"Model saved to {save_path}, and can be loaded via SentenceTransformer('{save_path}')")