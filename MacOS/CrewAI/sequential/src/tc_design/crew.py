from crewai import Crew, Process
from tasks import requirement_analysis_task, test_scenario_design_task, test_design_task, test_review_task
from agents import requirements_analyst, scenario_designer, test_designer, test_manager

# Forming the tech-focused crew with some enhanced configuration
crew = Crew(
    agents=[requirements_analyst, scenario_designer, test_designer, test_manager],
    tasks=[requirement_analysis_task, test_scenario_design_task, test_design_task, test_review_task],
    process=Process.sequential,
    verbose=True
)

# Define the input dictionary with the file path
input_file_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/business_requirements.txt'
summary_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/output/summary.txt'
test_scenarios_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/output/scenarios.txt'
test_cases_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/output/test_cases.txt'
final_tc_path = '/Users/maymach09/Documents/GenAI09/MacOS/CrewAI/Advanced/src/tc_design/output/final_tc.json'


# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={
    'business_requirements':input_file_path,
    'summary_path':summary_path,
    'test_scenarios_path':test_scenarios_path,
    'test_cases_path':test_cases_path,
    'final_tc_path':final_tc_path
    })

# Inspect the result structure
#print(result)
for task in crew.tasks:
    output = task.output.exported_output

    # Determine the output file based on the task name
    if task == requirement_analysis_task:
        output_file = summary_path
    elif task == test_scenario_design_task:
        output_file = test_scenarios_path
    elif task == test_design_task:
        output_file = test_cases_path
    elif task == test_review_task:
        output_file = final_tc_path
    else:
        continue

    # Write the output to the specified file
    with open(output_file, 'w') as f:
        if output_file.endswith('.json'):
            import json
            json.dump(output, f, indent=4)
        else:
            f.write(output)


# # Save the outputs to the specified files
# task_outputs = {
#     'requirement_analysis_task': 'summary_path',
#     'test_scenario_design_task': 'test_scenarios_path',
#     'test_design_task': 'test_cases_path',
#     'test_review_task': 'final_tc_path'
# }


# for task in crew.tasks:
#     output = task.get_output()
#     output_file_key = task_outputs[task.name]
#     output_file = result['inputs'][output_file_key]
    
#     with open(output_file, 'w') as f:
#         if output_file.endswith('.json'):
#             import json
#             json.dump(output, f, indent=4)
#         else:
#             f.write(output)

# print("Process completed successfully.")



# print(result)
