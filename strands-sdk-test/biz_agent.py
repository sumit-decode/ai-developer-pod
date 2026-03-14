import os
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel
from typing import List

# 1. Environment Configuration
os.environ["GROQ_API_KEY"] = "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"

# 2. Define the Structured Output Schema
class ProjectRequirements(BaseModel):
    project_summary: str
    user_roles: List[str]
    user_stories: List[str]
    acceptance_criteria: List[str]

# 3. Initialize the Groq LLM
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.environ["GROQ_API_KEY"]
)

# 4. Define the Business Analyst Agent
biz_agent = Agent(
    role="Business Analyst",
    goal="Convert the user's project idea into structured software requirements.",
    backstory="""You are an expert Business Analyst. 
    Your mission is to take high-level project ideas and break them down into 
    clear, technical requirements.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- CRITICAL CHANGE FOR COMBINED MODE ---
# 5. Define the Task OUTSIDE the main block so graph_agent.py can import it
biz_task = Task(
    description="Analyze the project: {topic}. Generate technical requirements.",
    expected_output="A structured JSON object with project_summary, user_roles, user_stories, and acceptance_criteria.",
    agent=biz_agent,
    output_json=ProjectRequirements 
)

# Keep this part so you can still run the file separately if you want!
if __name__ == "__main__":
    crew = Crew(agents=[biz_agent], tasks=[biz_task])
    print("### Starting the Virtual Pod: Business Analyst Stage ###")
    result = crew.kickoff(inputs={"topic": "Build a collaborative markdown editor"})
    
    print("\n--- FINAL JSON OUTPUT ---")
    if result.pydantic:
        print(result.pydantic.model_dump_json(indent=2))