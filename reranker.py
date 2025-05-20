from FlagEmbedding import FlagReranker

reranker =  FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

def rerank_documents(query: str, initial_docs: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
    sentence_pairs = [[query, passage] for passage in initial_docs]
    scores = reranker.compute_score(sentence_pairs)
    score_document = [{"score": score, "content": content} for score, content in zip(scores, initial_docs)]
    result = sorted(score_document, key=lambda x: x["score"], reverse=True)[:top_n]
    return result

merged_chunks = kb_context + ([net_summary] if net_summary else [])
reranked = rerank_documents(rewrite, merged_chunks, top_n=10)
