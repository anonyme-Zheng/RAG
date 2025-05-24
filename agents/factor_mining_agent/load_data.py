# agents/factor_mining_agent/load_data.py
import qlib
from qlib.data import D
import pandas as pd
from qlib.constant import REG_CN

!python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
provider_uri = "~/.qlib/qlib_data/cn_data"  # 目标目录
qlib.init(provider_uri=provider_uri, region=REG_CN)

def init_qlib():
    """初始化qlib"""
    qlib.init(provider_uri=provider_uri, region=REG_CN)


def load_stock_data(instruments="csi300", start_time="2018-01-01", end_time="2023-12-31"):
    """加载股票数据"""
    data = D.features(
        instruments=instruments,
        fields=["$change", "$factor", "$low", "$volume", "$close", "$high", "$open"],
        start_time=start_time,
        end_time=end_time
    )
    return data

def get_factor_data(factor_expression, instruments="csi300", start_time="2018-01-01", end_time="2023-12-31"):
    """计算因子数据"""
    try: 
        factor_data = D.features(
            instruments=instruments,
            fields=[factor_expression],
            start_time=start_time,
            end_time=end_time
        )
        return factor_data
    except Exception as e:
        raise ValueError(f"因子计算失败: {e}")
