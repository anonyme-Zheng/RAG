import re
from openai_client import client


def rewrite_query(history_dialogue: str, query: str):
  
    prompt = f"""
根据上下文历史对话对用户的**金融相关咨询** query 进行改写，补全代词、明确主体，转为标准检索语句，非口语化，同时提取关键词（如公司、股票、财报、指标等）。

【历史对话】最近5轮
{history_dialogue}

【query】
{query}

【参考例子】
- 历史对话
human: 我想了解贵州茅台今年的市盈率
bot: 贵州茅台的市盈率目前约为35倍。
human: 那平安银行呢？
- 输出结果  
改写后的query: 平安银行 2025 年最新市盈率是多少？  
提取的关键词: 平安银行, 市盈率, 2025

- 历史对话
human: 你能告诉我上证指数最近一周的涨跌幅吗？
bot: 最近一周上证指数涨幅约 1.2%。
human: 成分股里表现最好的前五名哪些？
- 输出结果  
改写后的query: 上证指数成分股最近一周涨跌幅排名前五的股票代码及名称？  
提取的关键词: 上证指数, 成分股, 涨跌幅, 前五

请直接输出：  
改写后的query:  
提取的关键词:
""".lstrip()

    
    resp = client.chat.completions.create(
        model="qwen2.5-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = resp.choices[0].message.content.strip()

    # 从返回文本中提取改写后的 query
    match_q = re.search(r"改写后的query\s*[:：]\s*(.+)", content)
    rewrite = match_q.group(1).strip() if match_q else query

    # 从返回文本中提取关键词列表
    match_kw = re.search(r"提取的关键词\s*[:：]\s*(.+)", content)
    keywords = [k.strip() for k in match_kw.group(1).split(",")] if match_kw else []

    return rewrite, keywords, content
