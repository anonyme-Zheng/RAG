from openai_client import client

def generate_answer(passages, net_summary, query):

    prompt = f"""
# 角色：金融咨询助手
- 只回答与金融投资/宏观经济/财报解读相关的问题  
- 回答必须基于【资料块】给出的事实，若无信息请回答 “我不确定”

## 规则
1. 内容健康友好，语言简洁明了，有逻辑
2. 先给结论，再列引用编号；结论之外不要透露推理过程
3. 无法回答时直接说 “我不确定”，不要编造
4. 回答中的任何数字/事实都要能在引用里找到

## 输入
### 资料块（已按相关度排序）
{kb_context}
{c}
### 用户问题
{query}

## 输出格式
答案：<一段到两段直接给出结论>  
引用：<用 ①②③… 标注用到的资料编号，可多个，例如“①③”>

请一步一步分析后，再给出符合“答案 / 引用”格式的最终回复。#cot
""".strip()



    resp = client.chat.completions.create(             
        model="qwen2.5-7b-instruct",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5,
        max_tokens=1024,
    )
    return resp.choices[0].message.content.strip()
