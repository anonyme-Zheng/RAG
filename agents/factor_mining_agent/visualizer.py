# agents/factor_mining_agent/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns

class FactorVisualizer:
    def plot_ic_analysis(self, ic_series):
        """绘制IC分析图"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # IC时序图
        axes[0,0].plot(ic_series)
        axes[0,0].set_title('IC Time Series')
        
        # IC分布直方图
        axes[0,1].hist(ic_series, bins=30)
        axes[0,1].set_title('IC Distribution')
        
        return fig
    
    def plot_factor_return(self, factor_returns):
        """绘制因子收益图"""
        # 累计收益曲线等
        pass
