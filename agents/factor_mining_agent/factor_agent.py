# agents/factor_mining_agent/factor_agent.py
import json
from datetime import datetime
from pathlib import Path

from agents.factor_mining_agent.query_rewriter import rewrite_query_for_factor_agent
from agents.factor_mining_agent.factor_generator import generate_factor_formula
from agents.factor_mining_agent.load_data import get_factor_data, init_qlib
from agents.factor_mining_agent.factor_evaluator import FactorEvaluator
from agents.factor_mining_agent.factor_storage import save_factor, load_factor_library

# 初始化qlib
init_qlib()

# 初始化评估器
evaluator = FactorEvaluator()

def process_factor_request(query: str, history: str = ""):
    """处理因子挖掘请求"""
    # 1. 重写查询
    rewrite, params, _ = rewrite_query_for_factor_agent(history, query)
    
    # 2. 判断意图：构造因子 or 回测因子
    if "因子构造" in rewrite:
        return create_factor(rewrite, params)
    elif "因子回测" in rewrite:
        return backtest_factor(rewrite, params)
    else:
        return "无法识别的因子操作请求"

def create_factor(rewrite: str, params: list):
    """创建新因子"""
    try:
        # 从重写的查询中提取因子描述
        description = rewrite.split("｜")[1] if "｜" in rewrite else rewrite
        
        # 生成因子公式
        formula = generate_factor_formula(description)
        
        # 计算因子数据进行初步验证
        factor_data = get_factor_data(formula)
        
        # 评估因子
        return_data = get_factor_data("Ref($close, -1)/$close - 1")  # 简单收益率
        eval_results = evaluator.evaluate_factor(factor_data, return_data)
        
        # 保存因子到因子库
        factor_info = {
            "name": f"Factor_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "formula": formula,
            "description": description,
            "ic_mean": eval_results['ic_mean'],
            "ic_ir": eval_results['ic_ir'],
            "create_time": datetime.now().isoformat()
        }
        
        save_factor(factor_info)
        
        return f"""
因子构造成功！
公式：{formula}
IC均值：{eval_results['ic_mean']:.4f}
IC_IR：{eval_results['ic_ir']:.4f}
因子已保存到因子库。
"""
    except Exception as e:
        return f"因子构造失败：{str(e)}"

