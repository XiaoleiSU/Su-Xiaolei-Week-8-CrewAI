from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task

load_dotenv()


def build_llm() -> LLM:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    if not api_key:
        print("Missing DEEPSEEK_API_KEY in .env", file=sys.stderr)
        sys.exit(1)
    if "your-key-here" in api_key:
        print("DEEPSEEK_API_KEY is still a placeholder in .env", file=sys.stderr)
        sys.exit(1)
    return LLM(model=model, api_key=api_key, base_url=base_url)


def build_crew(llm: LLM) -> Crew:
    data_analyst = Agent(
        role="Senior Data Analyst",
        goal="Turn business context into churn-relevant findings.",
        backstory="You specialize in subscription analytics and evidence-first reporting.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    root_cause_analyst = Agent(
        role="Root Cause Analyst",
        goal="Identify and rank likely churn causes from available evidence.",
        backstory="You connect behavior signals to churn using testable hypotheses.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    strategy_consultant = Agent(
        role="Customer Retention Strategy Consultant",
        goal="Design retention and win-back actions tied to root causes.",
        backstory="You advise on lifecycle, pricing, product, and service interventions.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    task_data_analysis = Task(
        description=(
            "Customer and business context:\n{customer_context}\n\n"
            "Deliver a structured brief:\n"
            "1) Metrics/cohorts/segments implied or stated.\n"
            "2) Patterns most relevant to churn.\n"
            "3) Data gaps and what to measure next.\n"
            "Do not invent numbers; mark assumptions clearly."
        ),
        expected_output="English brief: Metrics/Segments, Patterns, Data Gaps.",
        agent=data_analyst,
    )

    task_root_causes = Task(
        description=(
            "Use the previous task output from context. Produce ranked churn root causes. "
            "For each cause include evidence, mechanism, confidence (high/medium/low), "
            "and validation data needed."
        ),
        expected_output="English root-cause memo with ranking and confidence.",
        agent=root_cause_analyst,
        context=[task_data_analysis],
    )

    task_strategy = Task(
        description=(
            "Use both earlier outputs from context. Propose retention + win-back actions, "
            "including quick wins (0-30 days), medium-term moves (1-3 months), KPIs, and risks. "
            "Map every recommendation to at least one root cause."
        ),
        expected_output="English retention playbook mapped to root causes.",
        agent=strategy_consultant,
        context=[task_data_analysis, task_root_causes],
    )

    return Crew(
        agents=[data_analyst, root_cause_analyst, strategy_consultant],
        tasks=[task_data_analysis, task_root_causes, task_strategy],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    default_context = (
        "B2C SaaS: Monthly churn rose from 3.1% to 4.8% over two quarters. "
        "Cohorts with incomplete onboarding churn more. Discount-heavy cohorts churn faster. "
        "Customers using advanced features weekly show higher NPS."
    )
    customer_context = sys.argv[1] if len(sys.argv) > 1 else default_context
    result = build_crew(build_llm()).kickoff(inputs={"customer_context": customer_context})
    print("\n--- Final output ---\n")
    print(result)


if __name__ == "__main__":
    main()
