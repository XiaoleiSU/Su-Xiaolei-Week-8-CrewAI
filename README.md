# README — Brief Documentation and Reflection

## Business Problem
This crew addresses a customer churn problem in a subscription-style business. The goal is to explain why churn increased, identify the most likely root causes, and produce practical retention and win-back actions that a business team can execute in the short and medium term.

## How the 3 Agents Work Together
The crew runs in a strict sequential flow. First, the **Data Analyst** converts raw business context into a structured churn brief (metrics, segment patterns, and data gaps). Second, the **Root Cause Analyst** consumes that brief and ranks the likely causes of churn with evidence, causal logic, confidence, and validation needs. Third, the **Customer Retention Strategy Consultant** uses both previous outputs to design a retention playbook with quick wins, medium-term initiatives, KPIs, and risks. This design ensures each task builds on prior outputs through task context rather than generating isolated answers.

## Challenges Encountered and How I Solved Them (CrewAI Setup)
I encountered multiple setup and runtime issues while getting CrewAI working end-to-end. The first challenge was Python compatibility: newer CrewAI versions were not available for Python 3.14 in this environment, so I switched to Python 3.12 in a virtual environment. The second challenge was LLM provider access and authentication (403/401 errors). I resolved this by parameterizing the LLM configuration through environment variables and moving to a compatible provider setup. I also validated that `.env` values were correctly loaded and added safeguards for placeholder keys. After these fixes, the full sequential run completed successfully with outputs from all three agents.

## One Thing I Would Change with More Time
If I had more time, I would add **visual analytics charts** to make results easier for non-technical stakeholders to interpret. For example, I would include trend charts for churn rate by cohort, a funnel chart for onboarding completion, and a dashboard mapping root causes to retention initiatives and KPI targets.
