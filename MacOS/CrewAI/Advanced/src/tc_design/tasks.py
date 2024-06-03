# from crewai import Task
# from tools import web_tool, file_read_tool, file_write_tool
# from agents import requirements_analyst, scenario_designer, test_designer, test_manager


# # requirements analyst task
# requirement_analysis_task = Task(
#     description=(
#         "Analyze the {business_requirements}. Provide a summary of the key requirements."
#     ),
#     expected_output='requirement_summary',
#     tools=[file_read_tool,file_write_tool],
#     agent=requirements_analyst,
# )

# # scenario design task
# test_scenario_design_task = Task(
#     description=(
#         "Create test scenarios based on the requirement summary. Provide a"
#         " list of scenarios that cover all the key aspects."
#     ),
#     expected_output=(
#         "A list of test scenarios in the following format:\n"
#         "- Test Scenario Id: [Unique identifier]\n"
#         "- Test Scenario Name: [Brief name]\n"
#         "- Test Scenario Description: [Detailed description of the scenario]\n"
#     ),
#     agent=scenario_designer,
# )

# # Test design task
# test_design_task = Task(
#     description=(
#         "Develop detailed test cases from the test scenarios. Ensure that all edge cases"
#         " are covered.Ensure that test cases also cover both positive and negative cases."  
#     ),
#     expected_output=(
#         "A list of test cases in the following format:\n"
#         "- Test Scenario Id:: [Id from previous agent]\n"
#         "- Test case Id: [Unique identifier]\n"
#         "- Test Case Name: [Brief name]\n"
#         "- Test Case Description: [Detailed description about the test case]\n"
#         "- Preconditions: [Preconditions for the test]\n"
#         "- Test Steps: [Step-by-step procedure]\n"
#         "- Expected Results: [Expected outcome]"
#     ),
#     agent=test_designer,
# )

# # Review task
# test_review_task = Task(
#     description=(
#         "Review the designed test scenarios and test cases. Make any necessary modifications"
#         " and provide the final output in JSON format. Make sure to validate the following:\n"
#         "- Each test case is accurate and complete.\n"
#         "- All the requirements are thoroughly covered by the test cases.\n"
#         "- The test cases are robust and cover edge cases.\n"
#         "- Test cases cover both negative and positive cases.\n"
#         "- Test cases cover integration cases.\n"
#         "- Test cases cover functional and non-functional cases.\n"
#         "- Test cases cover database cases.\n"
     
#     ),
#     expected_output=(
#         "List of finalized test scenarios."
#         "Finalized test cases in JSON format with the following keys:\n"
#         "Test Case Id: [Unique identifier]\n"
#         "Test Case Name: [Brief name]\n"
#         "Test Case Description: [Detailed description about the test case]\n"
#         "Preconditions: [Preconditions for the test]\n"
#         "Test Steps: [Step-by-step procedure]\n"
#         "Expected Result: [Expected outcome]\n"
#     ),
#     tools=[file_write_tool],
#     agent=test_manager,
# )
#-------------------------------
from crewai import Task
from tools import file_read_tool, file_write_tool
from agents import requirements_analyst, scenario_designer, test_designer, test_manager

# Requirements analyst task
requirement_analysis_task = Task(
    description=(
        "Analyze the {business_requirements}. Provide a summary of the key requirements."
    ),
    expected_output='requirement_summary',
    tools=[file_read_tool, file_write_tool],
    agent=requirements_analyst,
)

# Scenario design task
test_scenario_design_task = Task(
    description=(
        "Create test scenarios based on the {requirement_summary}. Provide a"
        " list of scenarios that cover all the key aspects."
    ),
    expected_output='test_scenarios',
    tools=[file_read_tool, file_write_tool],
    agent=scenario_designer,
)

# Test design task
test_design_task = Task(
    description=(
        "Develop detailed test cases from the {test_scenarios}. Ensure that all edge cases"
        " are covered. Ensure that test cases also cover both positive and negative cases."
    ),
    expected_output='test_cases',
    tools=[file_read_tool, file_write_tool],
    agent=test_designer,
)

# Review task
test_review_task = Task(
    description=(
        "Review the designed test scenarios and test cases from {test_cases}. Make any necessary modifications"
        " and provide the final output in JSON format. Make sure to validate the following:\n"
        "- Each test case is accurate and complete.\n"
        "- All the requirements are thoroughly covered by the test cases.\n"
        "- The test cases are robust and cover edge cases.\n"
        "- Test cases cover both negative and positive cases.\n"
        "- Test cases cover integration cases.\n"
        "- Test cases cover functional and non-functional cases.\n"
        "- Test cases cover database cases.\n"
    ),
    expected_output='final_test_cases',
    tools=[file_write_tool],
    agent=test_manager,
)

