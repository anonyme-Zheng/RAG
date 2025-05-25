import pandas as pd
import numpy as np

def evaluate_simple(df):
    """
    只计算：年化收益、夏普、日均换手、最大回撤
    假设 df 是 multiindex 列，第一层 '1day'，第二层含 'account','turnover'…
    """
    # 先把列降成一级
    if isinstance(df.columns, pd.MultiIndex):
        df = df['1day']
    # 取净值和换手
    nav      = df['account']      # 资金净值
    turnover = df['turnover']     # 日换手率
    
    # 1) 年化收益
    daily_ret   = nav.pct_change().dropna()
    total_years = len(daily_ret) / 252
    total_ret   = nav.iloc[-1] / nav.iloc[0] - 1
    annual_ret  = (1 + total_ret) ** (1/total_years) - 1
    
    # 2) 年化波动 & 夏普
    ann_vol = daily_ret.std() * np.sqrt(252)
    sharpe  = annual_ret / ann_vol if ann_vol != 0 else np.inf
    
    # 3) 日均换手率（原来 annual_turn = turnover.mean() * 252）
    daily_turn = turnover.mean() 
    
    # 4) 最大回撤
    running_max = nav.expanding().max()
    drawdown    = (nav - running_max) / running_max
    max_dd      = drawdown.min()
    
    return {
        'Annual_Return':   annual_ret,
        'Sharpe_Ratio':    sharpe,
        'Daily_Turnover':  daily_turn,
        'Max_Drawdown':    max_dd,
    }

def print_simple(results):
    print("==== 简化版回测指标 ====")
    print(f"年化收益率     : {results['Annual_Return']:.2%}")
    print(f"夏普比率       : {results['Sharpe_Ratio']:.3f}")
    print(f"日均换手率     : {results['Daily_Turnover']:.2%}")
    print(f"最大回撤       : {results['Max_Drawdown']:.2%}")


res = evaluate_simple(df1)
print_simple(res)
