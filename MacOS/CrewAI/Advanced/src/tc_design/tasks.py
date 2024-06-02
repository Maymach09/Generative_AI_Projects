from crewai import Task
from tools import web_tool, file_tool
from agents import requirements_analyst, test_designer, test_manager

# Analyst task
requirements_analyst_task = Task(
    description=(
        "Analyze the provided {business_requirements} thoroughly. Identify and outline all key requirements, "
        "ensuring no aspect is overlooked. Your goal is to transform these requirements into high-level test scenarios "
        "that comprehensively cover all functional and non-functional aspects of the software changes."
    ),
    expected_output=(
        "A comprehensive list of test scenarios in the following format:\n"
        "- Requirement: [Requirement description]\n"
        "- Test Scenario Id: [Unique identifier]\n"
        "- Test Scenario Name: [Brief name]\n"
        "- Test Scenario Description: [Detailed description of the scenario]\n"
    ),
    tools=[file_tool],
    agent=requirements_analyst,
)

# Test design task
test_design_task = Task(
    description=(
        "Using the test scenarios provided by the Requirements Analyst, design detailed test cases. "
        "Additionally, research and apply relevant test design techniques to enhance the quality of your test cases. "
        "Incorporate both positive and negative test cases to ensure robustness."
    ),
    expected_output=(
        "A comprehensive list of test cases in JSON format with the following keys:\n"
        "- Test Case Id: [Unique identifier]\n"
        "- Test Case Name: [Brief name]\n"
        "- Preconditions: [Preconditions for the test]\n"
        "- Test Steps: [Step-by-step procedure]\n"
        "- Expected Result: [Expected outcome]\n"
    ),
    tools=[web_tool],
    agent=test_designer,
)

# Review task
test_review_task = Task(
    description=(
        "Review the test cases designed by the Test Designer. Your task is to ensure that:\n"
        "- Each test case is accurate and complete.\n"
        "- All the requirements are thoroughly covered by the test cases.\n"
        "- The test cases are robust and cover edge cases.\n"
        "- Test cases cover both negative and positive cases.\n"
        "- Test cases cover integration cases.\n"
        "- Test cases cover functional and non-functional cases.\n"
        "- Test cases cover database cases.\n"
        "If any of the above conditions are not met, then make necessary modifications to enhance "
        "the quality and completeness of the test cases, ensuring they align with project requirements and standards."
    ),
    expected_output=(
        "A comprehensive list of reviewed and possibly modified test cases in JSON format with the following keys:\n"
        "- Test Case Id: [Unique identifier]\n"
        "- Test Case Name: [Brief name]\n"
        "- Preconditions: [Preconditions for the test]\n"
        "- Test Steps: [Step-by-step procedure]\n"
        "- Expected Result: [Expected outcome]\n"
    ),
    tools=[web_tool, file_tool],
    agent=test_manager,
)