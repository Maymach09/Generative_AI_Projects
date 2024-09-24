from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st
import json

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
openai_api_key = os.environ.get('OPENAI_API_KEY')
print(openai_api_key)

CHROMA_PATH = "chroma"
tc_format_path = "/Users/maymach09/Documents/GenAI09/MacOS/RAG_TestCases/tc_json_format"
#prompt = "prompt.txt"

# Load the JSON format from a separate file
with open(tc_format_path, "r") as json_file:
    tc_json_format = json.load(json_file)

# Convert the JSON format to a string
tc_format_str = json.dumps(tc_json_format, indent=4)


PROMPT_TEMPLATE = """

---------------------------------------------------------------------
User Prompt for Generating Test Cases:
---------------------------------------------------------------------

You are an intelligent assistant tasked with generating comprehensive test cases for software based on specific requirements detailed in the \
provided document content. The user will specify a requirement of the software for which they need test cases. \
Use the information from the document and the topic provided by the user to generate relevant and thorough test cases.

Document Content:
{context}

Requirement:
{scenario}

Instructions for Test Case Generation:
	1	Identify Key Requirements:
	2	Extract key functional and non-functional requirements from the provided document relevant to the specified topic.
	3	Understand the User's Topic:
	4	Focus on the specific aspect or feature mentioned by the user. Ensure your test cases cover all possible scenarios related to this aspect.
	5	Generate Test Cases:
	6	Create detailed test cases including:
	    •	Test Case ID: Unique identifier for each test case.
        •	Title: A concise title summarizing the test case.
        •	Description: Detailed description of what the test case is verifying.
        •	Preconditions: Any setup or prerequisites needed before executing the test.
        •	Test Steps: Step-by-step instructions to execute the test.
        •	Expected Results: The expected outcome of each step or the entire test case.
        •	Postconditions: Any cleanup or state reset needed after test execution.
	7	Consider Edge Cases:
	8	Include edge cases and boundary conditions to ensure comprehensive coverage.
	9	Format Output:
	10	Format the output clearly, making it easy for testers to understand and execute.

Example User Input and Test Case:

Requirement: Generate test cases for the user authentication feature.

Generated Test Cases:
{output_format}

----------------------------------------------------------------------------------------------------------
Generate your test cases following this structure and ensure they are detailed, clear, and thorough.
----------------------------------------------------------------------------------------------------------

If user's input is not relevant to the document content then do not generate the test cases and just say "Invalid question, please enter a valid input"

"""

def main():
    
    # streamlit framework
    st.title("AI Tester")
    topic = st.text_area("Enter a Requirement:")
    

    if topic:
        try:
            # Prepare the  DB
            embedding = OpenAIEmbeddings()
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
           
           # Search the DB.
            results = db.similarity_search_with_relevance_scores(topic, k=2)
            if len(results) == 0 or results[0][1] < 0.6:
                st.write(f"Unable to find matching results.")
                return
            else:
                st.write(results)
            #Prepare prompt
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, scenario=topic, output_format=tc_format_str)
            st.write(prompt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        model = ChatOpenAI(api_key=openai_api_key, temperature=0.4)
        response_text = model.predict(prompt)

        # Assuming response_text contains the JSON string
        response_data = json.loads(response_text)

        # Convert the response data back to a JSON-formatted string with indentation
        formatted_json = json.dumps(response_data, indent=4)

        sources = [f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})" for doc, _score in results]
        
        formatted_response = f"Response: {formatted_json}"
        
        #print document soource
        st.write(f"\nSource Document: \n\n{sources}")

        # print output test cases
        st.text_area("Formatted Response", value=formatted_response, height=400)

if __name__ == "__main__":
    main()