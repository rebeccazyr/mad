import json
from torch.utils.data import Dataset


class TripletContrastiveDataset(Dataset):
    def __init__(self, claim_to_evidences_path, evidence_id_to_sentence_path, claim_id_to_claim_path):
        with open(claim_to_evidences_path, "r") as f:
            self.claim_to_evidences = json.load(f)
        with open(evidence_id_to_sentence_path, "r") as f:
            self.evidence_id_to_sentence = json.load(f)
        with open(claim_id_to_claim_path, "r") as f:
            self.claim_id_to_claim = json.load(f)

        # Filter out samples with empty positive_ids or negative_ids
        self.samples = []
        for claim_id, evidence_dict in self.claim_to_evidences.items():
            pos_ids = evidence_dict.get("positive_ids", [])
            neg_ids = evidence_dict.get("negative_ids", [])
            if len(pos_ids) > 0 and len(neg_ids) > 0:
                self.samples.append((claim_id, evidence_dict))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        claim_id, evidence_dict = self.samples[idx]
        claim_text = self.claim_id_to_claim[claim_id]

        # Get positive evidence sentences
        pos_ids = evidence_dict["positive_ids"]
        pos_sentences = [self.evidence_id_to_sentence[str(pid)] for pid in pos_ids]

        # Get negative evidence sentences
        neg_ids = evidence_dict["negative_ids"]
        neg_sentences = [self.evidence_id_to_sentence[str(nid)] for nid in neg_ids]

        return claim_text, pos_sentences, neg_sentences
