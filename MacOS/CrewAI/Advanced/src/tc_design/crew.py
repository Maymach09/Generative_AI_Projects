from crewai import Crew, Process
from tasks import requirement_analysis_task, test_scenario_design_task, test_design_task, test_review_task
from agents import requirements_analyst, scenario_designer, test_designer, test_manager

# Forming the tech-focused crew with some enhanced configuration
crew = Crew(
    agents=[requirements_analyst, scenario_designer, test_designer, test_manager],
    tasks=[requirement_analysis_task, test_scenario_design_task, test_design_task, test_review_task],
    process=Process.sequential,
)

# Define the input dictionary with the file path
input_file_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/business_requirements.txt'

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'business_requirements':input_file_path})
print(result)
