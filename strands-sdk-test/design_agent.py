import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# Ensure temperature is 0 for stability
llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.0)

@tool("write_design_artifact")
def write_design_artifact(filename: str, text: str) -> str:
    """Saves a design file. Parameters: filename, text."""
    try:
        # 1. Reject if empty
        if not text or len(text.strip()) < 5:
            return "ERROR: Text is too short."

        os.makedirs("design", exist_ok=True)
        
        # 2. THE ULTIMATE CLEANER: 
        # Extract only the content before the model starts rambling again
        # We also strip out any accidental JSON or XML tags the model might hallucinate
        clean_content = text.split("<function")[0].split("---")[0].strip()
        clean_content = clean_content.replace("```", "")
        
        file_path = os.path.join("design", filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_content)
            
        return f"SUCCESS: {filename} saved ({len(clean_content)} chars)."
    except Exception as e:
        return f"ERROR: {str(e)}"

@tool("save_final_plan")
def save_final_plan(text: str) -> str:
    """Saves the final plan.md file. Provide ONLY a simple list."""
    try:
        os.makedirs("design", exist_ok=True)
        # We strip everything to ensure no garbage is saved
        clean_content = text.split("<function")[0].replace("`", "").strip()
        with open("design/plan.md", "w", encoding="utf-8") as f:
            f.write(clean_content)
        return "SUCCESS: plan.md saved."
    except Exception as e:
        return f"ERROR: {str(e)}"

# Update your Agent to use ONLY this tool for the final step
design_agent = Agent(
    role="Architect",
    goal="Save technical blueprints.",
    backstory="You are a minimalist. You provide ONLY the tool call.",
    llm=llm,
    tools=[write_design_artifact, save_final_plan], # Add the new tool here
    verbose=True
)

design_task = Task(
    description="""Review requirements: {requirements}.
    Save 3 files using 'write_design_artifact':
    1. 'api.yaml': Full OpenAPI Spec.
    2. 'schema.sql': Full SQL Tables.
    3. 'plan.md': A simple numbered list of 5 steps.
    
    CRITICAL: 
    - For 'plan.md', do NOT use '#' headers. Just use plain text and numbers.
    - Do NOT use markdown backticks.
    - If a tool fails, simplify the text and try again.""",
    expected_output="3 files saved with real content.",
    agent=design_agent
)