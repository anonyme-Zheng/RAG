from openai_client import client

def need_search(kb_context: str, query: str) -> bool:
    """
    判断是否需要进行外部检索。

    参数:
        kb_context: 已检索到的本地知识上下文（多条文本拼接的字符串）
        query:      用户的原始问题

    返回:
        True  —— 需要外部搜索 (DO_SEARCH)
        False —— 本地资料足够 (NO_SEARCH)
    """
   
    prompt = f"""
你是金融对话系统中的检索判断助手，请判断资料是否足够回答用户的问题。
- 如果资料中找不到确切事实/数据，请返回：DO_SEARCH
- 如果回答中可能出现“我不确定”或需要编造，请返回：DO_SEARCH
- 只有当答案**确定且能明确支持**用户问题时才返回：NO_SEARCH

【已检索到的内部资料】
{kb_context}

【用户问题】
{query}

只输出 NO_SEARCH 或 DO_SEARCH。
""".lstrip()

    
    resp = client.chat.completions.create(
        model="qwen2.5-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    result = resp.choices[0].message.content.strip()

    return result == "DO_SEARCH"

