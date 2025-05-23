# agents/factor_mining_agent/backtester.py
import qlib
from qlib.workflow import R
from qlib.utils import init_instance_by_config
import yaml

class FactorBacktester:
    def __init__(self, config_path="configuration.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def backtest_factor(self, factor_expression: str, start_date: str, end_date: str):
        """执行因子回测"""
        # 动态更新配置中的因子表达式
        self.config['task']['dataset']['kwargs']['handler']['kwargs']['fields'] = [factor_expression]
        
        # 运行回测
        recorder = R.get_recorder()
        model = init_instance_by_config(self.config['task']['model'])
        dataset = init_instance_by_config(self.config['task']['dataset'])
        
        # 训练和预测
        model.fit(dataset)
        
        # 获取回测结果
        port_analysis = recorder.load_object("portfolio_analysis")
        return port_analysis
