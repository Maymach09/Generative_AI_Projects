from agents import reviewer, test_designer
from crewai import Task

## Analyze Requirements Task

review = Task(
  description=(
    "1. Analyze the {user_requirements}.\n"
    "2. Based on the analysis write test scenarios which covers"
    " all the requirements.\n"
    "3. Assign a unique id to each scenario.\n"
    "4. Prioritize the requirements and assign them the priority"
    " from among: 'High', 'Medium', or 'low'.\n"
    "5. Assign the scenario type to each scenario from among:"
    " 'Functional', 'Regression' or 'Performance'"
  ),
  expected_output="Well structured test scenarios in JSON format with the following key-value pairs: \n"
   "Id:Value"
   "Test_Scenario:Value"
   "Priority:Value"
   "Type:Value" ,
  agent=reviewer,
)

## Test Designing task

design = Task(
    description=(
    "1. Analyze the {user_requirements}.\n"
    "2. Based on the analysis write detailed test cases which covers "
    "all the requirements.\n"
    "3. Each test case should have multiple numbered steps guiding the "
    "user on how to execute the test case.\n"
    "4. Assign a unique name to each test case "
    "with the following nomenclature: 'TCserialnumber_Functionality_Positive_Or_Negative'."
    "5. Prioritize the test cases and assign them the priority"
    "from among: 'High', 'Medium', or 'low'.\n"
    "6. Assign the test case type to each scenario from among:"
    "'Functional', 'Regression' or 'Performance'"
    ),
    expected_output="Well structured test cases in JSON format with the following key-value pairs:\n"
   "TC_Name:Value"
   "Test_Steps:Value"
   "Priority:Value"
   "Type:Value" ,
  agent=test_designer,
)