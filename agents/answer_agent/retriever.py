import es
from embedding import model

def retrieve(query: str, top_k: int = 5):
    """向 ES 发起检索，返回最相关的 chunk 列表"""
    q_vec = model.encode([query])[0].tolist()
    dsl = {
      "size": top_k,
      "query": {
        "script_score": {
          "query": {"match_all": {}},
          "script": {
            "source": "cosineSimilarity(params.qv, doc['chunk_vector']) + 1.0",
            "params": {"qv": q_vec}
          }
        }
      },
      "_source": True
    }
    resp = es.es.search(index="financial_report_data", body=dsl)

    snippets: list[str] = []
    for hit in resp["hits"]["hits"]:
        score = hit["_score"]
        source = hit["_source"]
        ticker = source.get("ticker", "")
        company = source.get("company_name", "")
        chunk = source.get("chunk", "")
        report_time = source.get("report_time", "")
        text = (
            f" [{score:.4f}] {company}（{ticker}）｜ {report_time}\n"
            f" {chunk}"
        )
        snippets.append(text)

    return snippets
