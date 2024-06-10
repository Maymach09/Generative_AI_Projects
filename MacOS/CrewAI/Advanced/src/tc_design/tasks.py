from crewai import Task
from tools import file_read_tool, file_write_tool
from agents import requirements_analyst, scenario_designer, test_designer, test_manager

# Requirements analyst task
requirement_analysis_task = Task(
    description=(
        "Analyze the {business_requirements} and provide a summary of the key requirements."
    ),
    expected_output= 'A summary of the key business requirements in bullet points.',
    Output_File=True,
    tools=[file_read_tool,file_write_tool],
    agent=requirements_analyst,
)

# Scenario design task
test_scenario_design_task = Task(
    description=(
        "Create test scenarios based on the requirements summary from requirements_analyst agent. Provide a"
        " list of scenarios that cover all the key aspects."
    ),
    expected_output='List of test scenarios',
    Output_File=True,
    tools=[file_write_tool],
    agent=scenario_designer,
)

# Test design task
test_design_task = Task(
    description=(
        "Develop detailed test cases from the test scenarios. Ensure that all edge cases"
        " are covered. Ensure that test cases also cover both positive and negative cases."
    ),
    expected_output=(
        'List of test cases with the following fields:\n'
        'Test Case Id\n'
        'Test Case Name\n'
        'Preconditions\n'
        'Test Steps\n'
        'Expected Outcome\n'
    )
    ,
    tools=[],
    agent=test_designer,
)

# Review task
test_review_task = Task(
    description=(
        "Review the designed test scenarios and test cases. Make any necessary modifications"
        " and provide the final output in JSON format. Make sure to validate the following:\n"
        "- Each test case is accurate and complete.\n"
        "- All the requirements are thoroughly covered by the test cases.\n"
        "- The test cases are robust and cover edge cases.\n"
        "- Test cases cover both negative and positive cases.\n"
        "- Test cases cover integration cases.\n"
        "- Test cases cover functional and non-functional cases.\n"
        "- Test cases cover database cases.\n"
    ),
    expected_output= (
                    'JSON format with the following key-value pairs:\n '
                     'Test Case Id: Unique identifier\n'
                     'Test Case Name: Unique Name with test type and functionality\n'
                     'Preconditions: Preconditions\n'
                     'Test Steps: Detailed Steps to execute the test cases\n'
                     'Expected Result: Expected outcome of the test case\n'
),
    Output_File=True,
    tools=[file_write_tool],
    agent=test_manager,
)

