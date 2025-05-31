import asyncio
from query_data import query_retriever
from langchain.schema import ChatMessage  # Ensure this matches your actual import
import pandas as pd

df = pd.read_csv("queries.csv")
ground_truth = {
    row["query_id"]: row["relevant_docs"].split(",")
    for _, row in df.iterrows()
}
retrieved = {}
def compute_metrics(retrieved: dict, ground_truth: dict, k: int = 5):
    """
    Compute MRR (Mean Reciprocal Rank), MAP (Mean Average Precision), and Recall@k.
    
    Args:
        retrieved: Dict of {query_id: [retrieved_doc_ids]} (ranked list)
        ground_truth: Dict of {query_id: [relevant_doc_ids]}
        k: Cutoff for Recall@k calculation
        
    Returns:
        Tuple of (MRR, MAP, Recall@k)
    """
    reciprocal_ranks = []
    average_precisions = []
    recalls = []

    for qid in ground_truth:
        gt_docs = set(ground_truth[qid])
        retrieved_docs = retrieved.get(qid, [])
        
        # MRR: Find the first relevant doc
        rr = 0.0
        for rank, doc in enumerate(retrieved_docs, start=1):
            if doc in gt_docs:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)
        
        # MAP: Compute precision at each relevant doc
        num_relevant_retrieved = 0
        precisions = []
        for i, doc in enumerate(retrieved_docs, start=1):
            if doc in gt_docs:
                num_relevant_retrieved += 1
                precisions.append(num_relevant_retrieved / i)
        ap = sum(precisions) / len(gt_docs) if gt_docs else 0.0
        average_precisions.append(ap)
        
        # Recall@k: Fraction of relevant docs found in top-k
        top_k_docs = set(retrieved_docs[:k])
        recall = len(top_k_docs & gt_docs) / len(gt_docs) if gt_docs else 0.0
        recalls.append(recall)

    # Aggregate metrics
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
    map_score = sum(average_precisions) / len(average_precisions) if average_precisions else 0.0
    recall_at_k = sum(recalls) / len(recalls) if recalls else 0.0

    return mrr, map_score, recall_at_k

def main():
    for _, row in df.iterrows():
        query_id = row["query_id"]
        question = row["query"]
        print(f"Processing query ID: {query_id}, Question: {question}")
        chat = [ChatMessage(role="system", content="You are a knowledgeable and compassionate medical assistant chatbot specialized in respiratory diseases. Your goal is to help users understand symptoms, conditions, prevention, and treatments related to the respiratory system. Always provide clear, concise, and medically accurate information based on trusted sources. Avoid repetition, stay focused on the specific question, and include practical advice when relevant."),
            ChatMessage(role="user", content=question)]
        sources = query_retriever(chat)
        retrieved[query_id] = sources
    print("Retrieved documents:", retrieved)
    print("Ground truth:", ground_truth)
    # Evaluate metrics
    print("Evaluating metrics...")
    mrr, map_score, recall_at_3 = compute_metrics(retrieved, ground_truth,k=3)
    print(f"Mean Reciprocal Rank (MRR): {mrr}")
    print(f"Mean Average Precision (MAP): {map_score}")
    print(f"Recall@3: {recall_at_3}")

if __name__ == "__main__":
    main()