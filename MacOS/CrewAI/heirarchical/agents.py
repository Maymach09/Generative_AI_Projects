from crewai import Agent
from tools import txt_read_tool, pdf_read_tool, file_write_tool, web_tool
from tools import llm

# Define Agents
test_manager = Agent(
    role='Test Manager',
    goal='Oversee the test planning process, assign tasks, review outputs and provide review comments back to the agent.',
    backstory="A seasoned test manager ensuring quality and thoroughness in the testing process.",
    verbose=True,
    memory=True,
    llm=llm,
    #tools=[file_read_tool,file_write_tool],
    allow_delegation=True
)

test_planner = Agent(
    role='Test Planner',
    goal='Create a comprehensive test plan based on the software requirements',
    backstory="An experienced test planner with a knack for identifying key testing areas.",
    verbose=True,
    memory=True,
    llm=llm,
    #tools=[file_read_tool,file_write_tool]
)

test_scenario_designer = Agent(
    role='Test Scenario Designer',
    goal='Develop detailed test scenarios based on the test plan',
    backstory="A creative thinker focused on covering all possible use cases.",
    verbose=True,
    memory=True,
    llm=llm,
    #tools=[file_read_tool,file_write_tool]
)

test_case_developer = Agent(
    role='Test Case Developer',
    goal='Write specific test cases based on the test scenarios using the best test techniques found online',
    backstory="A meticulous test case writer ensuring thorough coverage and clarity.",
    verbose=True,
    memory=True,
    llm=llm,
   # tools=[file_read_tool,file_write_tool,web_tool]
)