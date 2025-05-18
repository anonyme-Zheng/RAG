import argparse
import re
import uuid
from pathlib import Path
from typing import Iterator

from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from FlagEmbedding import FlagAutoModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm

load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=10,
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
)

model = FlagAutoModel.from_finetuned('BAAI/bge-large-zh-v1.5',
                                      query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                                      use_fp16=True)

def embed(texts: list[str]) -> list[list[float]]:
    
    emb = model.encode(
        texts,
        batch_size=64,
        max_length=512,      
    )
  
    return emb.tolist()

company_lookup: dict[str, str] = {
    "600030": "中信证券股份有限公司",
    "600036": "招商银行股份有限公司",
    "600276": "江苏恒瑞医药股份有限公司",
    "600519": "贵州茅台酒股份有限公司",
    "600900": "中国长江电力股份有限公司",
    "601166": "兴业银行股份有限公司",
    "601318": "中国平安保险（集团）股份有限公司",
    "601398": "中国工商银行股份有限公司",
    "601899": "紫金矿业集团股份有限公司",
    "688256": "中科寒武纪科技股份有限公司",
}

def gen_actions(txt_path: Path):
    ticker = txt_path.parent.name                 
    year_match = re.search(r"\d{4}", txt_path.stem)
    year  = year_match.group() if year_match else "0000"
    company = company_lookup.get(ticker, "未知公司") if company_lookup else "未知公司"
    
    text  = txt_path.read_text(encoding="utf-8")
    chunks = text_splitter.split_text(text)
    vecs   = embed(chunks)
    
    title = f"{company} {year} 年报"
    title_vec = embed([title])[0] 

    index_name = "financial_report_data"   

    for i, (chunk, vec) in enumerate(zip(chunks, vecs)):
        uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{ticker}_{year}_{i}"))
        yield {
            "_index": index_name,
            "_id":    uid,
            "_source": {
                "title":        title,
                "chunk":        chunk,
                "company_name": company,
                "doc_id":       uid,
                "ticker":       ticker,
                "report_time":  f"{year}-12-31 00:00:00",
                "title_vector": title_vec,
                "chunk_vector":  vec         
            }
}


def parse_args():
    p = argparse.ArgumentParser(description="Index TXT chunks into Elasticsearch")
    p.add_argument("--txt_dir", required=True, type=Path, help="TXT 根目录")
    p.add_argument("--es", default="http://localhost:9200", help="Elasticsearch URL")
    p.add_argument("--index", default="financial_report_data", help="索引名")
    return p.parse_args()

  

def main():
    args = parse_args()
    es = Elasticsearch(args.es, basic_auth=(os.getenv("ES_USER"), os.getenv("ES_PASS")))

    for txt_file in tqdm(list(args.txt_dir.rglob("*.txt")), desc="文件"):
        helpers.bulk(
            es,
            gen_actions(txt_file, args.index),
            chunk_size=512,
            request_timeout=120,
        )
        print(f" 已写入 {txt_file.relative_to(args.txt_dir.parent)}")


if __name__ == "__main__":
    main()
