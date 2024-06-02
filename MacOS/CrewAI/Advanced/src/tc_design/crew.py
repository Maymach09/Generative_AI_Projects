from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool

from crewai import Crew,Process
from tasks import requirements_analyst_task,test_design_task,test_review_task
from agents import requirements_analyst, test_designer, test_manager

## Forming the tech focused crew with some enhanced configuration
crew=Crew(
    agents=[requirements_analyst,test_designer, test_manager],
    tasks=[requirements_analyst_task,test_design_task, test_review_task],
    process=Process.sequential,

)


input_file_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/requirements.txt'

## starting the task execution process wiht enhanced feedback
result=crew.kickoff(inputs={'business_requirements':input_file_path})
print(result)