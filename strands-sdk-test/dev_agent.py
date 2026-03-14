import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.1)

# --- REFINED TOOLS TO PREVENT 400 ERRORS ---

@tool("dev_write_file")
def dev_write_file(filename: str, text: str) -> str:
    """Saves a file. Use for models.py and schemas.py."""
    os.makedirs("server", exist_ok=True)
    # Strip any extra text the LLM might add
    clean = text.split("<function")[0].replace("```python", "").replace("```", "").strip()
    with open(f"server/{filename}", "w", encoding="utf-8") as f:
        f.write(clean)
    return f"SUCCESS: {filename} saved."

# Use this to split main.py into small chunks if it's too long
@tool("dev_append_file")
def dev_append_file(filename: str, text: str) -> str:
    """Appends to a file. Use to build main.py in segments."""
    clean = text.split("<function")[0].replace("```python", "").replace("```", "").strip()
    with open(f"server/{filename}", "a", encoding="utf-8") as f:
        f.write("\n\n" + clean)
    return f"SUCCESS: Appended to {filename}."

dev_agent = Agent(
    role="FastAPI Developer",
    goal="Implement code in small stable chunks.",
    backstory="You are a modular coder. You write small snippets to avoid errors.",
    llm=llm,
    tools=[dev_write_file, dev_append_file],
    verbose=True
)

dev_task = Task(
    description="""Implement the Design. 
    Follow this order to prevent 400 errors:
    1. 'dev_write_file': filename='main.py', text='FastAPI imports and app init'
    2. 'dev_append_file': filename='main.py', text='User CRUD routes'
    3. 'dev_append_file': filename='main.py', text='Post CRUD routes'
    4. 'dev_append_file': filename='main.py', text='Moderation logic'
    
    CRITICAL: Keep each tool call SHORT. No backticks.""",
    expected_output="FastAPI app fully implemented in segments.",
    agent=dev_agent
)