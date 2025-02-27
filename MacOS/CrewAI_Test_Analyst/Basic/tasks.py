from agents import reviewer, test_designer, test_lead
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


lead = Task(
    description=(
    "Analyze the {user_requirements}. "
    "Review the response drafted by Software Requirements Reviewer based on {user_requirements}. "
    "Review the response drafter by Software Test Designer based on {user_requirements}. "
    "Verify that software testing designing techniques \n"
    "and industry standard software testing principles have been followed in the responses. "
    "Ensure that all the requirements are covered by the test scenarios and test cases. "
    "Also ensure that both positive and negative test cases have been covered in the responses.  "
    ),
    expected_output="Well structured test cases in JSON format with the following key-value pairs:\n"
   "TC_Name:Value"
   "Test_Steps:Value"
   "Priority:Value"
   "Type:Value" ,
  agent=test_lead,
)