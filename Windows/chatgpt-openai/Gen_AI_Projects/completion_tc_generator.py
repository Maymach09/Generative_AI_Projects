import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        openai.api_key = self.api_key
        messages = [{"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content

def summarize_requirements(requirements, client):
    prompt = f"""
    You are a product owner and your role is to provide clear requirements to the technical team for product development.
    Rewrite the following requirements delimited by triple backticks in JSON format with the following keys:
    - User Requirement Name (High Level Functionality)
    - USer Requirement Id (Serial Number)
    - User Requirement Description
    - User Requirement Priority
    - User Requirement Type
    If requirements are insufficient or if they do not make any sense to you then don't summarize them \
    instead just say "Requirements cannot be summarized."
    ```{requirements}```
    """
    summarized_requirements = client.get_completion(prompt)
    return summarized_requirements

def generate_code(requirements, client):
    prompt = f"""
    You are a software developer who writes code for any given user requirement in python.
    Your task is to write the entire python code which covers all the following requirements delimited by triple backticks.
    Make sure to add comments to each line of code explaining the purpose of the line.
    If requirements are insufficient or if they do not make any sense to you then don't generate code \
    instead just say "Code cannot be generated due to insufficient requirements."
    ```{requirements}```
    """
    code = client.get_completion(prompt)

    return code

def generate_test_cases(requirements, client):
    prompt = f"""
    You are a software tester, a bot who writes test cases for software applications and it's components.
    Create at least 2 test cases for each user requirement in the text delimited by triple backticks.
    If a user requirement needs more than 2 test cases then create all that are required.
    If requirements are insufficient or unclear just say that "Test cases cannot be generated due to \
    insufficient requirements."
    Provide test cases in JSON format with the following keys:
    - test_case_name (High Level Functionality_LowLevelFunctionality_TestCaseType_Serial Number)
    - pre_condition
    - steps_to_execute (series of actions)
    - expected_result
    ```{requirements}```
    """
    test_cases = client.get_completion(prompt).strip()
    return test_cases

def generate_traceability_matrix(requirements, test_cases, client):
    prompt = f"""
    You are a software tester, your job is to create a traceability matrix. This matrix maps the \
    user requirements with the generate test cases.
    Take each point from text delimited by triple backticks and map it to the relevant test case \
    from the text delimited by triple inverted commas.
    Generate traceability matrix in the JSON format with the following keys:
    - User Requirement Name
    - USer Requirement Id
    - Test Case Name
    ```{requirements}```
    '''{test_cases}'''
    
    """
    traceability_matrix = client.get_completion(prompt)

    return traceability_matrix