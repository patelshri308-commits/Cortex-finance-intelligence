****Cortex Finance Intelligence****

AI-native finance analytics workspace designed to automate recurring SaaS finance workflows using multi-agent orchestration, semantic business context, and executive-ready reporting automation.

⸻

**Overview**

Cortex Finance Intelligence is a simulated enterprise finance analytics platform inspired by modern AI-native analytics workflows.

The project demonstrates how finance organizations can operationalize AI-driven analysis on top of curated warehouse KPI models rather than relying on manual spreadsheet workflows.

The platform combines:

* KPI analytics pipelines
* semantic business definitions
* AI workflow orchestration
* specialized finance agents
* executive commentary generation
* reporting/export automation
* Streamlit-based analytics workspace

The project was intentionally designed to mirror concepts emphasized in modern enterprise analytics environments such as:

* AI-native workflow engineering
* semantic analytics
* finance reporting automation
* natural language analytics
* agentic workflow orchestration
* executive business intelligence systems

⸻

**Core Features**

Multi-Agent Finance Analytics System

The platform includes specialized finance workflow agents:

Agent	Purpose
Revenue Summary Agent	Generates executive SaaS revenue commentary
Variance Analysis Agent	Explains month-over-month business changes
Forecast Sensitivity Agent	Simulates scenario-based revenue forecasts
Executive Briefing Agent	Synthesizes multiple workflows into CFO-style briefings
Router Agent	Dynamically selects the correct workflow based on business intent

⸻

**Semantic Metrics Layer**

The platform includes a semantic business layer that defines:

* KPI business meaning
* interpretations
* metric definitions
* source mappings
* finance context

This allows AI workflows to reason about business metrics more consistently and accurately.

Example:

metric: total_arr
definition:
  Annual recurring revenue across active customers.
interpretation:
  Higher ARR indicates stronger recurring SaaS revenue performance.

⸻

**AI Finance Workspace**

Users interact with the system through a multi-page Streamlit application.

Workflows include:

* Executive KPI dashboard
* Natural-language finance analysis workspace
* Revenue performance analysis
* Variance commentary
* Forecast sensitivity modeling
* Executive briefing generation
* Excel reporting exports

⸻

**Reporting Automation**

The platform supports automated multi-tab Excel export generation.

Generated reports consolidate:

* KPI datasets
* AI-generated executive summaries
* variance analysis
* forecast sensitivity analysis
* executive leadership briefings

This simulates real finance reporting workflows used by:

* Strategic Finance
* FP&A
* Revenue Operations
* Executive leadership teams

⸻

**Architecture**

Synthetic SaaS Finance Data
            ↓
Databricks Warehouse Layer
            ↓
SQL KPI Models / Views
            ↓
Semantic Metrics Layer
            ↓
Router / Orchestration Layer
            ↓
Specialized AI Finance Agents
            ↓
Gemini LLM Reasoning
            ↓
Executive Commentary Generation
            ↓
Streamlit Analytics Workspace
            ↓
Excel Reporting Export

⸻

**Tech Stack**

Data / Analytics

* Python
* Pandas
* SQL
* Databricks
* Faker (synthetic data generation)

AI / Workflow Orchestration

* Google Gemini API
* YAML-based prompt skill architecture
* Multi-agent workflow orchestration
* Semantic business context injection

Frontend

* Streamlit
* Plotly

Reporting Automation

* OpenPyXL
* Excel export generation

⸻

**Why This Project Exists**

Traditional finance workflows often involve:

* repetitive SQL analysis
* spreadsheet-heavy reporting
* manual executive commentary
* repetitive forecast packaging
* disconnected analytics workflows

This project explores how AI-native workflow systems can operationalize and accelerate recurring finance analytics processes.

Instead of manually recreating the same analyses each week, the platform encodes finance workflows into reusable AI agents.

⸻

**Example Workflow**

Example user prompt:

What happens if churn increases by 10%?

System flow:

User Question
      ↓
Router Agent
      ↓
Forecast Sensitivity Agent
      ↓
Semantic Business Context Injection
      ↓
Gemini Reasoning
      ↓
Executive Forecast Commentary
      ↓
Excel / Streamlit Output

⸻

**Enterprise Concepts Demonstrated**

This project intentionally focuses on enterprise AI analytics architecture concepts such as:

* AI workflow orchestration
* semantic analytics
* multi-agent systems
* finance KPI modeling
* executive reporting automation
* reusable prompt workflows
* natural-language analytics
* AI-native business tooling
* warehouse-centric analytics systems

⸻

**Synthetic Data Disclaimer**

This project uses synthetic SaaS finance data generated programmatically for demonstration purposes.

The architecture and workflows are designed to simulate realistic enterprise finance analytics systems while avoiding the use of proprietary business data.

⸻

**Future Snowflake Migration Goals**

Planned future enhancements include migration toward:

* Snowflake Cortex Analyst
* Cortex Agents
* Dynamic Tables
* semantic views
* Snowflake-native Streamlit deployment
* warehouse-native AI orchestration
* natural-language semantic querying

⸻

**Running The Project**

Install Dependencies

pip install -r requirements.txt

⸻

**Generate Synthetic SaaS Data**

python3 scripts/generate_saas_data.py

⸻

**Run AI Agents**

Revenue Summary

python3 agents/revenue_summary_agent.py

Variance Analysis

python3 agents/variance_analysis_agent.py

Forecast Sensitivity

python3 agents/forecast_sensitivity_agent.py

Executive Briefing

python3 agents/executive_briefing_agent.py

⸻

**Launch Streamlit Workspace**

streamlit run app/main.py

⸻

**Generate Excel Finance Report**

python3 exports/excel_exporter.py

⸻

Repository Structure

agents/                 # AI finance workflow agents
app/                    # Streamlit application
exports/                # Reporting/export automation
semantic_models/        # Semantic KPI definitions
sql/                    # SQL warehouse models/views
prompts/                # YAML prompt skill files
outputs/                # Generated workflow outputs
scripts/                # Synthetic dataset generation
utils/                  # Shared utilities

⸻

**Key Takeaways**

This project is not intended to be a generic chatbot.

It is an AI-native finance workflow system designed to demonstrate how:

* curated warehouse KPIs
* semantic business context
* workflow orchestration
* specialized AI agents
* executive reporting automation

can be combined into a modern enterprise analytics platform.

The emphasis of the project is on workflow engineering and operational analytics systems rather than model training.

⸻

****Author****

**Shri Patel**

**LinkedIn:** https://www.linkedin.com/in/shripatel2003/
