# Purpose: Evaluates retrieval accuracy using cosine similarity.

from sentence_transformers import SentenceTransformer, util

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_retrieval(retrieved_docs, ground_truth):
    """Compute cosine similarity between retrieved docs and ground truth."""
    scores = [util.pytorch_cos_sim(
        embedding_model.encode(doc, convert_to_tensor=True),
        embedding_model.encode(ground_truth, convert_to_tensor=True)
    ).item() for doc in retrieved_docs]
    
    return sum(scores) / len(scores) if scores else 0
