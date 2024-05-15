from secret_key import OPENAI_API_KEY1
import langchain_QnA as lc
import os
import streamlit as st

def main_qa():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    # streamlit framework
    st.title("Software Testing QnA")
    user_input = st.sidebar.text_area("Ask a question:")

    #url = os.path.join('C:', 'Users', 'Mayan', 'OneDrive', 'Documents', 'GitHub', 'GenAI', 'Langchain', 'pdf_assistant', 'ISTQB_CTFL_Syllabus.pdf')

    url = 'C:\Documents\PDFs\ISTQB_CTFL_Syllabus.pdf'
    
    user_prompt = '''You are a Software Tester who is trained on the role is to create test cases for user given requirements.
                    Each test case that you write should be output in JSON format with the following keys:
                    1. Name of the test case in the format ApplicationName_Functionality_TypeOfTestCase_Order \
                    2. Pre-Conditions (if applicable) \
                    3. Steps to execute \
                    4. Expected result \
                    
                    If user input is not clear to you then ask user to be more specific instructions.
                  '''

    if user_input:
        try:
           response = lc.chatbot(url, user_input)
           #st.subheader("Generated Output:")
           st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")