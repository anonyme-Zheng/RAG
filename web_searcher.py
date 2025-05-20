from open_client import client

def web_search(query, num_results=5):
    prompt = f"""
你是一个金融领域的搜索摘要模拟器。请基于你的知识，对以下问题生成 {num_results} 条“类似搜索引擎摘要”的内容（每条包括标题和简短摘要，合计不超过200字），用于后续回答问题。
如果你不确定，不要编造。

问题：{query}

请使用如下格式：

1. 标题1
摘要1
2. 标题2
摘要2
...
"""
    resp = client.chat.completions.create(
        model="qwen-max-latest",
        messages=[{"role": "system", "content": "你是一个金融领域的搜索摘要模拟器。请基于你的知识，对以下问题生成 {num_results} 条“类似搜索引擎摘要”的内容（每条包括标题和简短摘要，合计不超过200字），用于后续回答问题。
如果你不确定，不要编造。"},
                   {"role": "user", "content": prompt}],
        extra_body={"enable_search": True,
                    "search_options": {            
        "forced_search": True,     
        "search_strategy": "pro"     } 
        },
        temperature=0.5
    )
    return resp.choices[0].message.content.strip()
