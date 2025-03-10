from crewai import Crew, Process
from tasks import assign_review_plan_task, test_plan_task, assign_review_scenario_task, test_scenario_task, assign_review_case_task, test_case_task
from agents import test_planner, test_scenario_designer, test_case_developer, test_manager
from tools import txt_read_tool, llm, pdf_read_tool

# Create Crew
crew = Crew(
    agents=[test_manager, test_planner, test_scenario_designer, test_case_developer],
    tasks=[assign_review_plan_task, test_plan_task, assign_review_scenario_task, test_scenario_task, assign_review_case_task, test_case_task],
    manager_llm=llm,
    process=Process.hierarchical,
)

# Kickoff Crew
#brd_content = txt_read_tool._run('/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/heirarchical/business_requirements.txt')
brd_content = pdf_read_tool._run('/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/heirarchical/DHM.pdf')

result = crew.kickoff(inputs={'software_requirements': brd_content})
print(result)