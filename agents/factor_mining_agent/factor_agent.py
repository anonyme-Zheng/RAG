# agents/factor_mining_agent/factor_agent.py
from factor_generator import generate_factor_formula
from factor_calculator import FactorCalculator
from backtester import FactorBacktester
from factor_evaluator import FactorEvaluator

class FactorMiningAgent:
    def __init__(self):
        self.calculator = FactorCalculator()
        self.backtester = FactorBacktester()
        self.evaluator = FactorEvaluator()
    
    def process_request(self, query: str, history: str = ""):
        """处理因子挖掘请求"""
        # 1. 查询重写
        rewritten_query, params, _ = rewrite_query_for_factor_agent(history, query)
        
        if "因子构造" in rewritten_query:
            return self.construct_factor(params)
        elif "因子回测" in rewritten_query:
            return self.backtest_factor(params)
        else:
            return "不支持的操作类型"
    
    def construct_factor(self, params):
        """构造因子"""
        # 从参数中提取因子描述
        description = params[0] if params else "动量因子"
        
        # 生成因子公式
        formula = generate_factor_formula(description)
        
        # 计算因子值
        factor_data = self.calculator.calculate_factor(formula, "2020-01-01", "2023-12-31")
        
        return f"因子构造完成：{formula}\n因子数据形状：{factor_data.shape}"
    
    def backtest_factor(self, params):
        """回测因子"""
        # 执行回测逻辑
        results = self.backtester.backtest_factor("factor_expression", "2020-01-01", "2023-12-31")
        return f"回测完成，年化收益率：{results.get('annual_return', 'N/A')}"
