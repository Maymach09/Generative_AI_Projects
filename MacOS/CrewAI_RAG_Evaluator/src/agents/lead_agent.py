# Purpose: Supervises and compiles evaluation scores.

from crewai import Agent

lead_agent = Agent(
    name="Supervisor",
    role="Oversees evaluation results.",
    goal="Compile final scores.",
    backstory="AI quality control specialist."
)
