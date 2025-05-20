from openai_client import client

def summarize(docs: str) -> str:
    n = docs.count("\n\n") + 1 if docs else 0
  
    prompt = """
请用商业财经专业语言，对下列{n}条网络搜索结果进行整合、去重，并在 200 字以内概括要点。若信息冲突请标注“不一致”。

{docs}

--- 200 字以内开始 ---
""".lstrip()
  
    resp = client.chat.completions.create(
        model="qwen2.5-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    return resp.choices[0].message.content.strip()
