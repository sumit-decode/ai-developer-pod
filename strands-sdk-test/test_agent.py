import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# High-throughput 8B model
llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.1)

@tool("save_test_file")
def save_test_file(text: str) -> str:
    """Saves tests/test_main.py. Accepts RAW Python pytest code."""
    try:
        os.makedirs("tests", exist_ok=True)
        clean = text.replace("```python", "").replace("```", "").strip()
        with open("tests/test_main.py", "w", encoding="utf-8") as f:
            f.write(clean)
        return "SUCCESS: tests/test_main.py saved."
    except Exception as e:
        return f"ERROR: {str(e)}"

test_agent = Agent(
    role="QA Engineer",
    goal="Verify API core logic.",
    backstory="""You are a precise tester. You write modular tests. 
    You ALWAYS call 'save_test_file' FIRST, then provide your summary report.""",
    llm=llm,
    tools=[save_test_file],
    verbose=True
)

test_task = Task(
    description="""Review the implemented code.
    
    1. Write exactly 5 critical test cases.
    2. Call 'save_test_file' using the 'text' parameter.
    3. Once the tool returns SUCCESS, provide the QA report as your FINAL ANSWER.
    
    REQUIRED SUMMARY FORMAT (Final Answer only):
    STATUS: [PASS/FAIL]
    TOTAL: [Number]
    PASSED: [Number]
    FAILED: [Number]
    """,
    expected_output="The QA summary report provided after saving the test file.",
    agent=test_agent
)