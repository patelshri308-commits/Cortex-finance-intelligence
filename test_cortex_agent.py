from src.workflow_logger import log_agent_run
from src.agent_loader import load_agent
from src.cortex_runner import run_cortex

print("Starting Cortex agent test...")

agent = load_agent("agents/revenue_analysis_agent.yaml")

prompt = f"""
ROLE:
{agent["role"]}

OBJECTIVE:
{agent["objective"]}

INSTRUCTIONS:
{chr(10).join(agent["instructions"])}

OUTPUT FORMAT:
{chr(10).join(agent["output_format"])}

Analyze this SaaS revenue scenario:

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

log_agent_run(
    agent_name=agent["agent_name"],
    model_name=agent["model"],
    workflow_type="revenue_analysis_test",
    prompt=prompt,
    response=response
)

print("\n===== CORTEX AGENT RESPONSE =====\n")
print(response)
