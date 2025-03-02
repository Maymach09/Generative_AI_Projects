# Purpose: Assigns retrieval evaluation task to the retrieval agent.

from crewai import Task
from agents.retrieval_agent import retrieval_agent
from evaluation.retrieval_evaluator import evaluate_retrieval

retrieval_task = Task(
    description="Evaluate retrieval relevance using cosine similarity.",
    agent=retrieval_agent,
    function=evaluate_retrieval,
    expected_output="Relevance Score (0-1)"
)
