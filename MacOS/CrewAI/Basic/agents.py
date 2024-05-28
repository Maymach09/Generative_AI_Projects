from crewai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"

## Create Agents

reviewer = Agent(
    role="Software Requirements Reviewer",
    goal="Analyze the {user_requirements} and write the high level test scenarios",
    backstory="You are working on reviewing some upcoming software changes"
              "based on the following requirements:{user_requirements}."
              "You review the information given to you and write the high level test scenarios."
              "Your work is the basis for the test designer to derive the comprehensive test cases"
              "which will be later executed to test the software's accuracy.",
    allow_delegation=False,
	verbose=True
)

test_designer = Agent(
    role="Software Test Designer",
    goal="Analyze the {user_requirements} and write comprehensive test cases.",
    backstory="Business provided some {user_requirements} for some software changes."
              "You are analyzing those requirements to derive the test cases based on them."
              "Your goal is to write test cases based on the industry standard software testing techniques"
              "like equivalence partitioning, boundary value analysis, decision table testing etc."
              "You also need to ensure that all the requirements are covered by the test cases"
              "so that the software changes can be tested comprehensively",
    allow_delegation=False,
    verbose=True
)   