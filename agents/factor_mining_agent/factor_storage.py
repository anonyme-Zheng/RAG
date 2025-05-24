# agents/factor_mining_agent/factor_storage.py
import json
from pathlib import Path
from typing import Dict, List

FACTOR_LIBRARY_PATH = Path("factor_library.json")

def save_factor(factor_info: Dict):
    """保存因子到因子库"""
    # 加载现有因子库
    factors = load_factor_library()
    
    # 添加新因子
    factors.append(factor_info)
    
    # 保存到文件
    with open(FACTOR_LIBRARY_PATH, 'w', encoding='utf-8') as f:
        json.dump(factors, f, ensure_ascii=False, indent=2)

def load_factor_library() -> List[Dict]:
    """加载因子库"""
    if not FACTOR_LIBRARY_PATH.exists():
        return []
    
    with open(FACTOR_LIBRARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_factors(keyword: str = None, min_ic: float = None) -> List[Dict]:
    """搜索因子库"""
    factors = load_factor_library()
    
    # 按关键词过滤
    if keyword:
        factors = [f for f in factors if keyword in f.get('description', '')]
    
    # 按IC阈值过滤
    if min_ic:
        factors = [f for f in factors if f.get('ic_mean', 0) >= min_ic]
    
    return factors
