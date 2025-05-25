# agents/factor_mining_agent/backtester.py
import pandas as pd
pd.DataFrame.last = lambda self, offset=None: self.tail(1)
pd.Series.last    = lambda self, offset=None: self.tail(1)
# 永远只取最后一行，忽略 offset；足够满足 Qlib 的需求

import qlib
import numpy as np
from qlib.constant import REG_CN
from qlib.data import D
from qlib.backtest import backtest
from qlib.contrib.strategy.signal_strategy import TopkDropoutStrategy

def backtester(factor: str, 
               topk: int = 30, 
               n_drop: int = 3,
               account: float = 10_000_000,
               start_date: str = "2017-01-03",
               end_date: str   = "2020-08-31") -> pd.DataFrame:
    """
    对单因子 `factor` 做 TopkDropout 回测，并返回 daily portfolio metrics。
    
    参数
    ----
    factor : str
        因子的表达式，例如 "Ref($close,20)/$close-1"
    topk : int
        每日选股数量
    n_drop : int
        每日替换的股票数量
    account : float
        初始资金
    start_date : str
        回测开始日期（闭区间），格式 "YYYY-MM-DD"
    end_date : str
        回测结束日期（闭区间），格式 "YYYY-MM-DD"
    
    返回
    ----
    df1 : pd.DataFrame
        MultiIndex 列 (freq, metrics)，其中 freq="1day"，
        metrics 包含 account, return, turnover, value, 等。
    """
    # 1) 初始化
    provider_uri = "~/.qlib/qlib_data/cn_data"
    qlib.init(provider_uri=provider_uri, region=REG_CN)
    
    market    = "csi300"
    benchmark = "SH000300"
    start_dt  = pd.Timestamp(start_date)
    end_raw   = pd.Timestamp(end_date)
    
    # 2) 交易日历：多补一天前的因子值
    cal      = pd.DatetimeIndex(D.calendar(start_time="2016-01-01", end_time=end_date))
    start_dt = cal[cal.get_loc(start_dt)]
    end_dt   = cal[-2]
    pre_dt   = cal[cal.get_loc(start_dt) - 1]
    print(f"实际回测 {start_dt.date()} → {end_dt.date()}，补齐前一日 {pre_dt.date()}")
    
    # 3) 取因子并填充 NaN
    fac = D.features(
        instruments    = D.instruments(market=market),
        fields         = [factor],
        start_time     = pre_dt.strftime("%Y-%m-%d"),
        end_time       = end_dt.strftime("%Y-%m-%d"),
    )
    
    fac = fac.sort_index().ffill().bfill()
    
    # 4) 策略 + 回测
    strategy = TopkDropoutStrategy(signal=fac, topk=topk, n_drop=n_drop)
    executor_cfg = {
        "class": "SimulatorExecutor",
        "module_path": "qlib.backtest.executor",
        "kwargs": {
            "time_per_step": "day",
            "generate_portfolio_metrics": True,
        },
    }
    print("开始回测 ...")
    pm_dict, ind_dict = backtest(
        start_time = start_dt,
        end_time   = end_dt,
        strategy   = strategy,
        executor   = executor_cfg,
        benchmark  = benchmark,
        account    = account,
        exchange_kwargs = {
            "limit_threshold": 0.095,
            "deal_price":      "close",
            "open_cost":       0.0005,
            "close_cost":      0.0015,
            "min_cost":        5,
        },
    )
    
    # 5) 合并所有频率下的 portfolio_metrics 为一个 DataFrame
    
    df1 = pd.concat(
        {freq: data for freq, (data, _) in pm_dict.items()},
        axis=1
    )
    
    return df1
