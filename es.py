from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["http://localhost:9200"],  
    request_timeout=30,
    max_retries=10,
    retry_on_timeout=True
)

create_index_body = {
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "title": { "type": "text" },
            "chunk": { "type": "text" },
            "company_name": { "type": "keyword" },
            "doc_id": { "type": "keyword" },
            "ticker": { "type": "keyword" },
            "report_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "title_vector": {
                "type": "dense_vector",
                "dims": 1024
            },
            "chunk_vector": {
                "type": "dense_vector",
                "dims": 1024
            }
        }
    }
}


if not es.indices.exists(index="financial_report_data"):  
    es.indices.create(index="financial_report_data", body=create_index_body)  
