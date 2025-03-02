# Purpose: Assigns generation evaluation task to the generation agent

from crewai import Task
from agents.generation_agent import generation_agent
from evaluation.generation_evaluator import evaluate_generation

generation_task = Task(
    description="Evaluate response accuracy using LLM scoring.",
    agent=generation_agent,
    function=evaluate_generation,
    expected_output="Quality Score (1-10)"
)
