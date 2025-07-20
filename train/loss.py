import torch
import torch.nn.functional as F

def batched_multi_positive_contrastive_loss(anchors, positives_list, negatives_list, temperature=0.05):
    """
    Batched multi-positive contrastive loss (InfoNCE style).
    
    Args:
        anchors: Tensor of shape (B, D) - B anchor embeddings
        positives_list: List of B tensors, each of shape (Pᵢ, D)
        negatives_list: List of B tensors, each of shape (Nᵢ, D)
        temperature: Scaling factor

    Returns:
        Scalar contrastive loss averaged over B anchors
    """
    total_loss = 0.0
    B = anchors.size(0)

    for i in range(B):
        anchor = F.normalize(anchors[i].unsqueeze(0), dim=1)       # (1, D)
        pos = F.normalize(positives_list[i], dim=1)                # (Pᵢ, D)
        neg = F.normalize(negatives_list[i], dim=1)                # (Nᵢ, D)

        sim_pos = torch.matmul(anchor, pos.T).squeeze(0) / temperature  # (Pᵢ,)
        sim_neg = torch.matmul(anchor, neg.T).squeeze(0) / temperature  # (Nᵢ,)

        denom = torch.sum(torch.exp(sim_pos)) + torch.sum(torch.exp(sim_neg))
        loss_terms = -sim_pos + torch.log(denom)
        total_loss += loss_terms.mean()

    return total_loss / B