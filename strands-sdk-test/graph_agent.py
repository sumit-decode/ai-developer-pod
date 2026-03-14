import os
import time
from typing import TypedDict
from langgraph.graph import StateGraph, END
from crewai import Crew

# Import all agents and tasks from your files
from biz_agent import biz_agent, biz_task
from design_agent import design_agent, design_task
from dev_agent import dev_agent, dev_task
from test_agent import test_agent, test_task

# Define the shared state
class PodState(TypedDict):
    task_description: str
    biz_requirements: str
    technical_design: str
    final_code: str
    test_results: str

# --- NODE FUNCTIONS ---

def business_node(state: PodState):
    print("\n" + "="*50 + "\nNODE: BUSINESS ANALYST\n" + "="*50)
    result = Crew(agents=[biz_agent], tasks=[biz_task]).kickoff(inputs={"topic": state['task_description']})
    return {"biz_requirements": str(result)}

def design_node(state: PodState):
    print("\n" + "="*50 + "\nNODE: DESIGNER\n" + "="*50)
    # 8B model needs a moment to reset TPM bucket
    time.sleep(30) 
    result = Crew(agents=[design_agent], tasks=[design_task]).kickoff(inputs={"requirements": state['biz_requirements']})
    return {"technical_design": str(result)}

def developer_node(state: PodState):
    print("\n" + "="*50 + "\nNODE: DEVELOPER\n" + "="*50)
    # Increase to 60 seconds to ensure all 4 tool calls have budget
    print("Refilling tokens (60s cooldown)...")
    time.sleep(60) 
    
    # ... rest of your code
    
    prompt_input = state['technical_design']
    if state.get('test_results') and "STATUS: FAIL" in state['test_results'].upper():
        prompt_input += f"\n\n🚨 FIX PREVIOUS BUGS FOUND BY QA:\n{state['test_results']}"
    
    result = Crew(agents=[dev_agent], tasks=[dev_task]).kickoff(inputs={"design": prompt_input})
    return {"final_code": str(result)}

def testing_node(state: PodState):
    print("\n" + "="*50 + "\nNODE: TESTING AGENT\n" + "="*50)
    # Crucial for 8B model stability
    time.sleep(30) 
    
    result = Crew(agents=[test_agent], tasks=[test_task]).kickoff(inputs={"code": state['final_code']})
    
    res_str = str(result)
    print("\n--- FINAL QA REPORT ---")
    for line in res_str.split('\n'):
        if any(k in line for k in ["STATUS:", "TOTAL:", "PASSED:", "FAILED:"]):
            print(f"📊 {line.strip()}")
            
    return {"test_results": res_str}

# --- CONDITIONAL ROUTING LOGIC ---

def should_continue(state: PodState):
    # Normalize results to uppercase for consistent checking
    results = state.get('test_results', "").upper()
    
    print(f"--- DEBUG: Router Checking Results ---")
    
    # Check for PASS and 0 FAILED cases
    # This handles "STATUS: PASS", "STATUS: [PASS]", and "FAILED: 0"
    if "PASS" in results and "FAILED: 0" in results:
        print("✅ ROUTER: All tests passed. Finishing Process.")
        return "end"
    else:
        print("❌ ROUTER: Tests failed or incomplete. Looping back to Developer.")
        return "developer"

# --- GRAPH CONSTRUCTION ---

workflow = StateGraph(PodState)

workflow.add_node("business", business_node)
workflow.add_node("design", design_node)
workflow.add_node("developer", developer_node)
workflow.add_node("testing", testing_node)

workflow.set_entry_point("business")
workflow.add_edge("business", "design")
workflow.add_edge("design", "developer")
workflow.add_edge("developer", "testing")

# The crucial loop back fix
workflow.add_conditional_edges(
    "testing",
    should_continue,
    {
        "developer": "developer", # Map the return string to the node name
        "end": END               # Map the return string "end" to the official END constant
    }
)

app = workflow.compile()

if __name__ == "__main__":
    problem = "Build a blog API with post history and admin moderation."
    
    # Pass 'Complete' to skip nodes that use these variables
    initial_state = {
        "task_description": problem,
        "biz_requirements": "Complete", 
        "technical_design": "Complete (Files exist in design/ folder)",
        "final_code": "",
        "test_results": ""
    }

    print("🚀 Resuming directly from Developer Node...")
    # Update entry point in workflow definition above this block if needed:
    # workflow.set_entry_point("developer") 
    
    app.invoke(initial_state, {"configurable": {"thread_id": "resume_final"}})