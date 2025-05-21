import re
from openai_client import client


def rewrite_query_for_factor_agent(history_dialogue: str, query: str):
    prompt = f"""
根据上下文历史对话对用户的因子挖掘需求，将用户输入的自然语言 query 改写成：
1. 如果意图是**构造因子**，则输出“因子构造指令”：标准化的计算公式和参数声明；
2. 如果意图是**回测因子**，则输出“回测指令”：包括回测标的、时间区间、评估指标等。

请补全代词、明确主体，去口语化，并提取核心参数（如因子公式、股票池、回测区间、评估指标等）。

【历史对话】最近5轮
{history_dialogue}

【query】
{query}

【示例1：构造因子】
human: “我想做一个三个月的动量因子”
bot: 
改写后的 query: 因子构造｜动量因子 = (过去 3 个月 收益率)；参数：窗口期 = 3 个月
提取的参数：动量因子, 收益率, 窗口期=3个月

【示例2：回测因子】
human: “帮我看看这个因子在中证500上表现”
bot:
改写后的 query: 因子回测｜在 中证500 指数成分股 上，回测 动量因子；期间：2018-01-01 至 2022-12-31；指标：年化收益、夏普比率、最大回撤
提取的参数：中证500, 动量因子, 2018-01-01 至 2022-12-31, 年化收益, 夏普比率, 最大回撤

请直接输出：
改写后的 query:
提取的参数:
""".lstrip()

    resp = client.chat.completions.create(
        model="qwen2.5-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = resp.choices[0].message.content.strip()

    # 提取输出
    match_q = re.search(r"改写后的 query\s*[:：]\s*(.+)", content)
    rewrite = match_q.group(1).strip() if match_q else query

    match_params = re.search(r"提取的参数\s*[:：]\s*(.+)", content)
    params = [p.strip() for p in match_params.group(1).split("，")] if match_params else []

    return rewrite, params, content
