from crewai import Agent
from tools import file_tool, web_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables
load_dotenv()


## call the gemini model
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                           verbose=True,
                           temperature=0.5,
                           google_api_key=os.getenv("GOOGLE_API_KEY"))

## Agent1 - Requirements Analyst

requirements_analyst=Agent(
    role="Senior Requirements Analyst",
    goal='Analyze the business requirement document and build an understanding of all the requirements',
    verbose=True,
    memory=True,
    backstory=(
        "As an experienced software test analyst you are an expert in understanding the software requirements "
        "and transform them into high level test scenarios. Your in-depth understanding of the requirements "
        "ensures that all the possible test scenarios are identified and covers all aspects of the software changes. "
        "These scenarios will be used by another agent to derive comprehensive test cases from them. "
        "Success of the project literally depends on how well this agent performs."
    ),
    tools=[file_tool],
    llm=llm,
    allow_delegation=True

)

## Agent2 - Software Test Designer

test_designer = Agent(
  role='Software Test Designer',
  goal='Analyze the test scenarios and derive test cases from them',
  verbose=True,
  memory=True,
  backstory=(
    "Over the years, you have gained expertise in designing the test cases for simple to complex software changes. "
    "You will browse the internet to find the test designing techniques which will make the test cases more robust. "
    "You will use the test scenarios identified by the Senior Requirements Analyst as base and the design techniques "
    "identified from the internet to design the test cases. Ensure that test cases should cover both positive and "
    "negative cases."  
  ),
  tools=[web_tool],
  llm=llm,
  allow_delegation=True
)

## Agent3 - Software Test Manager

test_manager = Agent(
  role='Software Test Manager',
  goal='To review the test cases designed by Software Test Designer and make modifications as necessary',
  verbose=True,
  memory=True,
  backstory=(
    "As a Senior Test Manager you are responsible for the delivery of quality products in production. To test "
    "the software product you need robust and comprehensive test cases designed by your team members. "
    "You have enormous experience in the business domain and in software testing field. You will review all the " 
    "test cases designed by your team members and make sure that they are accurate, complete and covers all the " 
    "{business_requirements}"  
  ),
  tools=[web_tool, file_tool],
  llm=llm,
  allow_delegation=False
)