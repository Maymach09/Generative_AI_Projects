# Purpose: Agent responsible for evaluating retrieval relevance.

from crewai import Agent

retrieval_agent = Agent(
    name="Retrieval Evaluator",
    role="Analyzes retrieved documents for relevance.",
    goal="Score retrieval accuracy.",
    backstory="Expert in NLP and search retrieval."
)