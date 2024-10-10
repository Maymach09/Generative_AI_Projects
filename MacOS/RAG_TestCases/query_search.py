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

You are an experienced software tester tasked with generating comprehensive test cases for software based on specific requirements detailed in the \
provided document content below. The user will specify a requirement name of the software for which they need test cases. \
Use the information from the document and the requirement provided by the user to generate relevant and thorough test cases.

Document Content:
{context}

Requirement:
{scenario}

Follow the following instructions to generate test cases:

    1.	Identify Key Requirements:
	    •	Extract all relevant functional and non-functional requirements from the provided document that pertain to the specified feature or business requirement.
	2.	Understand the Focus Area:
	    •	Thoroughly grasp the user’s specified requirement or feature to ensure the test cases align with their expectations and cover all associated aspects.
	3.	Develop Comprehensive Test Cases:
	    •	For each requirement, generate detailed test cases that include:
            •	Test Case ID: A unique identifier for tracking.
            •	Title: A succinct yet descriptive title that captures the purpose of the test.
            •	Description: An in-depth explanation of what the test case will validate.
            •	Preconditions: Specify any conditions or configurations required before the test can be run.
            •	Test Steps: Clear, step-by-step instructions to carry out the test.
            •	Expected Results: The anticipated outcomes for each step or for the overall test case.
            •	Postconditions: Actions needed to reset or clean up the system after the test.
	4.	Ensure Thorough Coverage:
	    •	Incorporate both typical scenarios and edge cases (including boundary conditions) to guarantee complete testing coverage.
	5.	Output Format:
	    •	Ensure your response is in valid JSON format {output_format}


Example User Input and Test Case:

Requirement: Generate test cases for the user authentication feature.

Generated Test Cases:
{output_format}

----------------------------------------------------------------------------------------------------------
Generate your test cases following this structure and ensure they are detailed, clear, and thorough.
----------------------------------------------------------------------------------------------------------
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