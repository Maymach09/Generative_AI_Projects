from secret_key import OPENAI_API_KEY1
import fewshot as fs
import os
import streamlit as st


def main_fewshot():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    # streamlit framework
    user_input = st.text_input("Enter the requirement:")
    # Check if the user has entered a word
    if user_input:
        response = fs.testcase_fewshot(user_input)
        st.write(response)
