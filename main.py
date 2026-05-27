from src.agent_loader import load_agent
from src.cortex_runner import run_cortex

agent = load_agent("agents/revenue_analysis_agent.yaml")

prompt = f"""
ROLE:
{agent['role']}

OBJECTIVE:
{agent['objective']}

INSTRUCTIONS:
{chr(10).join(agent['instructions'])}

Please analyze this SaaS revenue scenario:

Q1 Revenue: $1.2M
Q2 Revenue: $1.6M
Enterprise customer growth: +18%
SMB churn increased by 9%
Infrastructure costs increased by 22%
"""

response = run_cortex(
    prompt=prompt,
    model=agent["model"]
)

print(response)