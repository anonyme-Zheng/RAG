import re
from openai import OpenAI

client = OpenAI()

# 支持的原始变量（使用时需加 $ 前缀）
ALLOWED_VARS = [
    "change", "factor", "low", "volume", "close", "high", "open"
]

# 支持的运算符
ALLOWED_OPS = [
    'Abs', 'Add', 'And', 'ChangeInstrument', 'Corr', 'Count', 'Cov', 'Delta',
    'Div', 'EMA', 'Eq', 'Feature', 'Ge', 'Greater', 'Gt', 'IdxMax', 'IdxMin',
    'If', 'Kurt', 'Le', 'Less', 'Log', 'Lt', 'Mad', 'Mask', 'Max', 'Mean',
    'Med', 'Min', 'Mul', 'Ne', 'Not', 'Or', 'P', 'PFeature', 'PRef', 'Power',
    'Quantile', 'Rank', 'Ref', 'Resi', 'Rolling', 'Rsquare', 'Sign', 'Skew',
    'Slope', 'Std', 'Sub', 'Sum', 'TResample', 'Var', 'WMA'
]


def validate_formula(formula: str) -> bool:
    """
    校验生成的公式只包含允许的变量（带 $）和运算符
    """
    tokens = re.findall(r"\$[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*", formula)
    for t in tokens:
        if t.startswith('$'):
            var = t[1:]
            if var not in ALLOWED_VARS:
                return False
        else:
            if t == '=' or t in ALLOWED_VARS:
                continue
            if t not in ALLOWED_OPS:
                return False
    return True


def generate_factor_formula(description: str) -> str:
    """
    根据自然语言描述，调用 LLM 生成因子公式，
    并校验结果满足规范。

    :param description: 因子功能的中文描述，例如“过去 5 天成交量加权平均价格的动量因子”。
    :return: 纯因子公式字符串，例如 "Momentum = Sub( Ref($volume,1), Ref($volume,5) )"
    """
    vars_list = ', '.join([f'${v}' for v in ALLOWED_VARS])
    ops_list = ', '.join(ALLOWED_OPS)
    prompt = f"""
你是一个因子构造助手，支持的原始变量（使用时需加 $）有：{vars_list}
支持的运算符有：{ops_list}

参考示例：
- 需求："过去 5 个交易日收盘价的 3 日 EMA 与 10 日 EMA 差值"
  输出：Momentum = Sub( EMA($close,3), EMA($close,10) )
- 需求："过去 10 日成交量加权平均价动量因子"
  输出：VWAP_Mom = Sub( Div( Sum( Mul($close,$volume), Rolling($volume,10) ), Rolling($volume,10) ),
                        Div( Sum( Mul($close,$volume), Rolling($volume,5) ), Rolling($volume,5) ) )

请根据以下需求描述，仅使用上述变量和运算符，生成一个符合语法的因子计算公式：
需求：{description}

仅输出因子公式，不要解释。
""".strip()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # 可替换为实际可用模型
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    formula = resp.choices[0].message.content.strip()

    if not validate_formula(formula):
        raise ValueError(f"生成公式不符合规范: {formula}")

    return formula


if __name__ == "__main__":
    desc = "过去 5 个交易日收盘价的 3 日 EMA 与 10 日 EMA 差值"
    formula = generate_factor_formula(desc)
    print("生成的因子公式：", formula)
