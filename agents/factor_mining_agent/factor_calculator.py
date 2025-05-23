# agents/factor_mining_agent/factor_calculator.py
import qlib
from qlib.data import D
import pandas as pd

class FactorCalculator:
    def __init__(self):
        self.init_qlib()
    
    def init_qlib(self):
        qlib.init(provider_uri="~/.qlib/qlib_data/cn_data", region="cn")
    
    def calculate_factor(self, formula: str, start_date: str, end_date: str, universe: str = "csi300"):
        """计算因子值"""
        try:
            factor_data = D.features(
                instruments=universe,
                fields=[formula],
                start_time=start_date,
                end_time=end_date
            )
            return factor_data
        except Exception as e:
            raise ValueError(f"因子计算失败: {e}")
