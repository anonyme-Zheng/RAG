# agent_dispatcher.py
from agents.answer_agent.pipeline import run_pipeline as run_answer_agent
from agents.factor_mining_agent.factor_agent import FactorMiningAgent

class AgentDispatcher:
    def __init__(self):
        self.factor_agent = FactorMiningAgent()
    
    def dispatch(self, query: str, history: str = ""):
        # 判断是金融问答还是因子挖掘
        if any(keyword in query for keyword in ["因子", "回测", "构造", "策略"]):
            return self.factor_agent.process_request(query, history)
        else:
            return run_answer_agent(query, history)
