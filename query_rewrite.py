from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),               # 已写入环境变量
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def classify_query(history_dialogue, query):
    prompt_template = f"""
# role
意图分类器
## profile
根据历史对话对用户输入 query 进行意图分类。

[类别标签以及定义]
1.闲聊 - 不涉及任务、信息或咨询的随意聊天内容
2.擦边 - 涉及敏感词、性暗示、不适宜公开场合的内容
3.政治人物批判 - 包含对政府、官员或政策的负面评论（不包括正常的财经新闻咨询）
4.金融相关咨询 - 包括个股、行业、基金、指标、财务、估值、市场动态、经济数据等金融投资类问题

【参考例子】
query: pussy
label: 擦边

query: 特朗普退休了吗
label: 政治人物批判

query: 茅台股票波动大吗
label: 金融相关咨询

query: 贵州茅台今年财报发布了吗
label: 金融相关咨询

query: 你喜欢什么颜色？
label: 闲聊

【历史对话】（如果无历史请忽略）
{history_dialogue}

【用户query】
{query}

请直接输出query的分类标签（只需输出“闲聊”/“擦边”/“政治人物批判”/“金融相关咨询”中的一个，不要其他多余文字）。

""".strip()

    response = client.chat.completions.create(
        model="qwen2.5-1.5b-instruct",
        messages=[{"role": "user", "content": prompt_template}],
        temperature=0  # 分类推荐使用温度为 0 保守输出
    )

    return response.choices[0].message.content.strip()
