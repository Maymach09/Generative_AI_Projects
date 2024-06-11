from crewai import Agent
from tools import file_read_tool, file_write_tool, web_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()

# Call the gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

# Agent1 - Requirements Analyst
requirements_analyst = Agent(
    role="Requirements Analyst",
    goal='Gather and analyze business requirements.',
    verbose=True,
    memory=True,
    backstory=(
        "You are responsible for understanding and analyzing the business requirements"
        " to ensure all aspects are covered for generating test scenarios and cases."
    ),
    tools=[file_read_tool,file_write_tool],
    llm=llm,
    allow_delegation=False
)

# Agent2 - Software Test Designer
scenario_designer = Agent(
    role="Test Scenario Generator",
    goal='Create test scenarios based on the analyzed requirements.',
    verbose=True,
    memory=True,
    backstory=(
        "Your job is to develop comprehensive test scenarios that cover all aspects of the"
        " business requirements to ensure thorough testing."
    ),
    tools=[file_write_tool],
    llm=llm,
    allow_delegation=False
)

# Agent3 - Software Test Designer
test_designer = Agent(
    role='Test Case Designer',
    goal='Develop detailed test cases from the test scenarios.',
    verbose=True,
    memory=True,
    backstory=(
        "You create detailed test cases based on the provided test scenarios, ensuring"
        " all edge cases are covered."
    ),
    tools=[file_write_tool],
    llm=llm,
    allow_delegation=False
)

# Agent4 - Software Test Manager
test_manager = Agent(
    role='Software Test Reviewer',
    goal='Review and modify the generated test scenarios and test cases.',
    verbose=True,
    memory=True,
    backstory=(
        "You ensure the quality and accuracy of the generated test scenarios and test cases,"
        " making necessary modifications before the final output."
    ),
    llm=llm,
    tools=[file_write_tool],
    allow_delegation=False
)
