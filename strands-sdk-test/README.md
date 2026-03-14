AI Software Development Pod 🤖
A multi-agent autonomous system powered by LangGraph and CrewAI that transforms high-level project ideas into a fully functional, tested FastAPI backend.

🏗 System Architecture
The project uses a directed acyclic graph (DAG) with a circular feedback loop for quality assurance:

Business Analyst Node: Defines structured requirements.

Architect Node: Generates OpenAPI specs, SQL schemas, and implementation plans.

Developer Node: Implements modular Python code (FastAPI + SQLAlchemy).

Testing Node: Runs a pytest suite. If tests fail, it loops back to the Developer Node for bug fixing.

🚀 Getting Started
1. Prerequisites
Python 3.10+

A Groq API Key (Sign up at console.groq.com)

2. Installation
Clone the repository and install dependencies:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory:

Plaintext
GROQ_API_KEY=your_gsk_key_here
📁 Project Structure
graph_agent.py: The core LangGraph orchestrator.

biz_agent.py: Logic for the Business Analyst.

design_agent.py: Logic for generating architectural blueprints.

dev_agent.py: Modular developer logic using "append" tools.

test_agent.py: logic for QA and automated testing.

design/: (Generated) Contains api.yaml, schema.sql, and plan.md.

server/: (Generated) Contains main.py, models.py, and schemas.py.

tests/: (Generated) Contains test_main.py.

🛠 Usage
To start the full autonomous loop:

Bash
python graph_agent.py
Resuming from a specific node
If the process hits a rate limit or a tool error after the design is already complete, you can update graph_agent.py to resume directly from the developer stage:

Python
# In graph_agent.py
workflow.set_entry_point("developer")
⚠️ Important Notes on Rate Limits
This project is optimized for the Llama-3.1-8b-instant model on Groq.

TPM Protection: Nodes include a time.sleep(30) to avoid "Rate limit reached" errors.

Modular Writing: The developer agent writes code in small chunks (segments) to prevent JSON formatting errors commonly found in smaller LLMs.

📊 Summary Format
The system expects the Testing Agent to provide a report in this specific format to decide if the loop should finish:

Plaintext
STATUS: [PASS/FAIL]
TOTAL: [Number]
PASSED: [Number]
FAILED: [Number]