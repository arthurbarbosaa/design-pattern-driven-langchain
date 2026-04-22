from src.orchestrator import Orchestrator

with open("code_to_refactor.py", "r", encoding="utf-8") as f:
    code = f.read()

orchestrator = Orchestrator()
for chunk in orchestrator.agent.stream(
    {"messages": [{"role": "user", "content": f"Refactor: {code}"}]}, 
    stream_mode="updates"
):
    print("--- STEP ---")
    print(chunk)
