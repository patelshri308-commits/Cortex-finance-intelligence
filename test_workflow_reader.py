from src.workflow_reader import get_recent_agent_runs

runs = get_recent_agent_runs(limit=5)

print("\n===== RECENT AGENT RUNS =====\n")

for run in runs:
    print(f"ID: {run['ID']}")
    print(f"Agent: {run['AGENT_NAME']}")
    print(f"Model: {run['MODEL_NAME']}")
    print(f"Workflow: {run['WORKFLOW_TYPE']}")
    print(f"Created At: {run['CREATED_AT']}")
    print("-" * 40)
