# agents/factor_mining_agent/factor_evaluator.py
import pandas as pd
import numpy as np
from scipy import stats

class FactorEvaluator:
    def __init__(self):
        pass
    
    def evaluate_factor(self, factor_data: pd.DataFrame, return_data: pd.DataFrame):
        """评估因子效果"""
        results = {}
        
        # IC分析
        ic_series = self.calculate_ic(factor_data, return_data)
        results['ic_mean'] = ic_series.mean()
        results['ic_std'] = ic_series.std()
        results['ic_ir'] = results['ic_mean'] / results['ic_std']
        
        # 单调性分析
        results['monotonicity'] = self.calculate_monotonicity(factor_data, return_data)
        
        return results
    
    def calculate_ic(self, factor_data, return_data):
        """计算信息系数"""
        ic_list = []
        for date in factor_data.index.get_level_values(0).unique():
            factor_cross = factor_data.loc[date].dropna()
            return_cross = return_data.loc[date].dropna()
            
            common_stocks = factor_cross.index.intersection(return_cross.index)
            if len(common_stocks) > 10:
                ic = factor_cross.loc[common_stocks].corrwith(return_cross.loc[common_stocks])
                ic_list.append(ic.iloc[0])
        
        return pd.Series(ic_list)
