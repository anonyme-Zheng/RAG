import argparse
from pathlib import Path
from typing import List

from elasticsearch import helpers

import es
import embedding
import retriever
import intent_recognizer
import query_rewriter
import search_decider
import web_searcher
import reranker
import summarizer
import responder


def ingest_data(txt_dir: str) -> None:
    """Ingest TXT files under ``txt_dir`` into Elasticsearch."""
    for txt_file in Path(txt_dir).rglob("*.txt"):
        actions = list(embedding.gen_actions(Path(txt_file)))
        if actions:
            helpers.bulk(
                es.es,
                actions,
                chunk_size=512,
                request_timeout=120,
            )


def run_pipeline(query: str, history: str = "", top_k: int = 5) -> str:
    """Run the question answering pipeline."""
    # Retrieve from ES
    kb_chunks: List[str] = retriever.retrieve(query, top_k=top_k)
    kb_context = "\n\n".join(kb_chunks)

    # Check intent
    intent = intent_recognizer.classify_query(history, query)
    if intent != "金融相关咨询":
        return "非金融相关问题"

    # Rewrite query
    rewrite, keywords, _ = query_rewriter.rewrite_query(history, query)

    # Decide if external search is needed
    do_search = search_decider.need_search(kb_context, rewrite)
    net_summary = ""
    if do_search:
        web_docs = web_searcher.web_search(rewrite)
        net_summary = summarizer.summarize(web_docs)

    # Rerank combined context
    merged_docs = kb_chunks + ([net_summary] if net_summary else [])
    reranked = reranker.rerank_documents(rewrite, merged_docs, top_n=top_k)
    passages = [item["content"] if isinstance(item, dict) else item for item in reranked]
    final_context = "\n\n".join(passages)

    # Summarize passages after rerank
    summary = summarizer.summarize(final_context)

    # Generate final answer
    answer = responder.generate_answer(final_context, summary, query)
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run retrieval augmented pipeline")
    parser.add_argument("--txt_dir", help="TXT directory to ingest", default=None)
    parser.add_argument("--query", help="Question to ask", default=None)
    parser.add_argument("--history", help="History dialogue", default="")
    args = parser.parse_args()

    if args.txt_dir:
        ingest_data(args.txt_dir)

    if args.query:
        print(run_pipeline(args.query, args.history))
