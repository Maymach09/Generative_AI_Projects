from secret_key import OPENAI_API_KEY1
import agent_and_chains as tr
import os
import streamlit as st


def main_general_knowledge():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    user_question = st.text_input("Ask your question:")

    # Check if the user has selected a language
    if user_question:
        response = tr.gk_chatbot(user_question)
        st.subheader("Answer:")
        st.write(response) 

# UI function to call chain
def main_translator():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    # streamlit framework
    user_text = st.text_input("Enter text for translation:")
    user_language = st.text_input("Translate to:")

    # Check if the user has selected a language
    if user_text and user_language:
        response = tr.translator_chain(user_text, user_language)
        st.subheader("Generated Output:")
        st.write(response['text'])

# UI function to call simple sequential chain
def main_sentence():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    # streamlit framework
    user_input = st.text_input("Enter a word you want to find antonym for:")

    # Check if the user has selected a language
    if user_input:
        response = tr.simple_seq_chain(user_input)
        st.subheader("Generated Output:")
        st.write(response['output'])
           

# UI function to call sequential chain
def main_antonym_sentence():
    # Set OpenAI API Key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY1

    # streamlit framework
    user_text = st.text_input("Enter a word you want to find antonym for:")

    # Check if the user has selected a language
    if user_text:
        response = tr.seq_chain(user_text)
        st.subheader("Generated Output:")
        st.write("Antonym:", response['derived_word'])
        st.write("Sentence:", response['sentence'])

def main():
    st.title("Langchain Demo UI")

    # Create tabs using the sidebar
    st.sidebar.title('Navigator')
    tabs = ['Translator', 'Create Sentence', 'Find Antonym and Create Sentence', 'General Knowledge']
    selected_tab = st.sidebar.radio('Go to', tabs)

    if selected_tab == 'Translator':
        main_translator()
    elif selected_tab == 'Create Sentence':
        main_sentence()
    elif selected_tab == 'Find Antonym and Create Sentence':
        main_antonym_sentence()
    elif selected_tab == 'General Knowledge':
        main_general_knowledge()