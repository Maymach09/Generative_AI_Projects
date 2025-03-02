# Purpose: Agent responsible for evaluating generated responses.

from crewai import Agent

generation_agent = Agent(
    name="Generation Evaluator",
    role="Evaluates AI-generated responses for quality.",
    goal="Rate accuracy and coherence of responses.",
    backstory="Linguistics expert."
)
