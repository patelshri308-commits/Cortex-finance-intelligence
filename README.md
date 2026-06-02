****Cortex Finance Intelligence****

AI-native finance analytics workspace designed to automate recurring SaaS finance workflows using multi-agent orchestration, semantic business context, and executive-ready reporting automation.

**Live Demo:** https://cortex-finance-intelligence.streamlit.app/

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

```yaml
metric: total_arr
definition:
  Annual recurring revenue across active customers.
interpretation:
  Higher ARR indicates stronger recurring SaaS revenue performance.
```

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

```
Synthetic SaaS Finance Data
         ↓
Snowflake Cortex CLI
         ↓
SQL KPI Models / Views
         ↓
Semantic Metrics Layer
         ↓
Router / Orchestration Layer
         ↓
Specialized AI Finance Agents
         ↓
Snowflake Cortex AI Reasoning
         ↓
Executive Commentary Generation
         ↓
Streamlit Analytics Workspace
         ↓
Excel Reporting Export
```

The platform uses a router-agent architecture built on Snowflake Cortex.

User Query
→ Router Agent
→ Semantic Resolver
→ KPI Context Layer
→ Specialized Finance Agent
→ Response

Specialized agents include:

- Revenue Summary Agent
- Variance Analysis Agent
- Forecast Sensitivity Agent
- Executive Briefing Agent

This design allows finance questions to be routed to purpose-built workflows instead of relying on a single general-purpose prompt.

⸻

** Semantic Business Metric Layer**

The platform includes a semantic finance layer that translates business concepts into relevant KPI context.

Examples:

Revenue Health
→ ARR
→ New ARR Bookings
→ Expansion ARR
→ Churned ARR
→ Contraction ARR
→ Net Revenue Impact

Revenue Quality
→ Expansion ARR
→ Churned ARR
→ Contraction ARR
→ Renewal Revenue

The semantic layer uses deterministic parent-child concept expansion to improve natural-language understanding and ensure consistent KPI analysis.

**Tech Stack**

Data / Analytics

* Python
* Pandas
* SQL
* Snowflake Cortex CLI
* Faker (synthetic data generation)

AI / Workflow Orchestration

* Snowflake Cortex AI
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

**## Evaluation Framework

The project includes a multi-layer evaluation framework designed to measure AI workflow quality.

### Router Evaluation

Validates that finance questions are routed to the correct specialized agent.

Current Performance:
- 20/20 test cases passed
- 100% routing accuracy

### Semantic Evaluation

Validates semantic concept detection and parent-child metric expansion.

Current Performance:
- 4/4 test cases passed
- 100% semantic accuracy

### End-to-End Evaluation

Validates generated responses against expected business concepts and quality requirements.

Current Performance:
- 3/3 test cases passed
- 100% pass rate

## Executive Dashboard

The Streamlit dashboard provides executive-level finance visibility including:

- KPI scorecards
- ARR trend analysis
- Monthly growth metrics
- ARR Bridge analysis
- Underlying KPI data inspection

ARR Bridge analysis helps explain how recurring revenue changed over time:

Ending ARR =
Starting ARR
+ New ARR Bookings
+ Expansion ARR
- Churned ARR
- Contraction ARR

**## Forecast Sensitivity Analysis

The platform supports interactive forecast scenarios through a dedicated Forecast Sensitivity Agent.

Users can model changes to:

- ARR Growth
- New ARR Bookings
- Expansion ARR
- Churned ARR
- Contraction ARR

The system generates executive-ready commentary describing financial impact, revenue risk, and potential business outcomes.**

**Example Workflow**

Example user prompt:

```
What happens if churn increases by 10%?
```

System flow:

```
User Question
     ↓
Router Agent
     ↓
Forecast Sensitivity Agent
     ↓
Semantic Business Context Injection
     ↓
Snowflake Cortex AI Reasoning
     ↓
Executive Forecast Commentary
     ↓
Excel / Streamlit Output
```

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

**Powered by Snowflake Cortex**

This platform leverages Snowflake as the central data and AI engine through:

* Snowflake Cortex CLI for semantic analysis and SQL KPI models
* Native Snowflake SQL for warehouse transformations
* Cortex AI integration for intelligent financial reasoning
* Seamless data governance and security across the platform
* Scalable enterprise warehouse architecture

⸻

**Running The Project**

Install Dependencies

```bash
pip install -r requirements.txt
```

⸻

**Generate Synthetic SaaS Data**

```bash
python3 scripts/generate_saas_data.py
```

⸻

**Run AI Agents**

Revenue Summary

```bash
python3 agents/revenue_summary_agent.py
```

Variance Analysis

```bash
python3 agents/variance_analysis_agent.py
```

Forecast Sensitivity

```bash
python3 agents/forecast_sensitivity_agent.py
```

Executive Briefing

```bash
python3 agents/executive_briefing_agent.py
```

⸻

**Launch Streamlit Workspace**

```bash
streamlit run app/main.py
```

⸻

**Generate Excel Finance Report**

```bash
python3 exports/excel_exporter.py
```

⸻

**Repository Structure**

```
agents/                 # AI finance workflow agents
app/                    # Streamlit application
exports/                # Reporting/export automation
semantic_models/        # Semantic KPI definitions
sql/                    # SQL warehouse models/views
prompts/                # YAML prompt skill files
outputs/                # Generated workflow outputs
scripts/                # Synthetic dataset generation
utils/                  # Shared utilities
```

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
