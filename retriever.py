from elasticsearch import Elasticsearch
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
    resp = es.search(index="financial_report_data", body=dsl)
    return [hit["_source"] for hit in resp["hits"]["hits"]]
