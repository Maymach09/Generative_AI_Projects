import os
from openai import OpenAI
import time

def get_file_path(file_name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_directory, 'dataset', file_name)

def upload_file(file_path):
    file = client.files.create(
    file=open(file_path, "rb"),
    purpose="assistants"
    )

    return file

def create_assistant(name, prompt, file):

    # Check if an assistant with the given name already exists
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            return assistant
    
    # If the assistant doesn't exist, create a new one
    assistant = client.beta.assistants.create(
        instructions=prompt,
        name=name,
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-0125",
        file_ids=[file.id]
    )
    return assistant

def initiate_chat(user_message, thread):
    if thread == None:
        thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

    return thread

def start_assistant(assistant, thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    processed_messages = set()

    print("Entering assistant loop...")

    while True:
        time.sleep(10)
        print("Checking status...")
        try:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            ).status
            print("Run status:", run_status)
        except Exception as e:
            print(f"Error occurred while retrieving run status: {e}")
            break

        if run_status == 'completed':
            break

        try:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
        except Exception as e:
            print(f"Error occurred while retrieving messages: {e}")
            break
        
        print("Retrieved messages:", len(messages.data))
        for message in messages.data:
            print("Processing message:", message.id)
            if message.id not in processed_messages and message.role == 'assistant':
                processed_messages.add(message.id)

    print("Assistant loop exited.")

    # Once status is completed, retrieve and print all assistant messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_messages = [content.text.value for message in messages.data if message.role == 'assistant' for content in message.content]
    return assistant_messages

def setup_assistant_and_chat(assistant_name, system_message, user_message):
    assistant = create_assistant(assistant_name, system_message, file)
    thread = initiate_chat(user_message, thread=None)
    return assistant, thread


if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI()
    file_name = 'claims_requirements.json'
    file_path = get_file_path(file_name)
    file = upload_file(file_path)
    

    assistant_name = "AI Tester"
    system_message = f"""
    As a professional software tester, your task is to analyze the requirements provided by the user and \
    generate test cases accordingly. Below file, delimited by triple backticks, contains the requirements.
    Use this information to formulate comprehensive test cases.
    ```{file.id}```
    """

    requirement_id = "13"
    number_of_test_cases = "5"
    user_message = f"""
    Provide {number_of_test_cases} critical test cases for requirement {requirement_id}.
     Response should strictly be in JSON format with the following keys: \
    - test_case_name: Follow the format Functionality_TestType_SerialNumber.
    - pre_condition: Describe any prerequisites or initial conditions.
    - steps_to_execute: Outline the actions to be taken.
    - expected_result: Specify the expected outcome after executing the test case.
    """

    assistant, thread = setup_assistant_and_chat(assistant_name, system_message, user_message)
    print("Loading1....")
    start_assistant(assistant, thread)
    assistant_responses = start_assistant(assistant, thread)
    print("Loading2....")
    for response in assistant_responses:
        print(response)


