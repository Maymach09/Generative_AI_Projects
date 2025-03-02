'''
Purpose:
✅ Defines CrewAI team with agents and tasks.
✅ Provides run_crew() function for execution.
'''

from crewai import Crew
from agents.retrieval_agent import retrieval_agent
from agents.generation_agent import generation_agent
from agents.lead_agent import lead_agent
from tasks.retrieval_task import retrieval_task
from tasks.generation_task import generation_task

# Initialize Crew with agents and tasks
crew = Crew(
    agents=[retrieval_agent, generation_agent, lead_agent],
    tasks=[retrieval_task, generation_task]
)

def run_crew():
    """Executes all tasks assigned to the Crew."""
    crew.kickoff()
