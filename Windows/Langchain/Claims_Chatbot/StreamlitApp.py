import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ChatMessageHistory
from src.claimsChatBot.bot import read_pdf, split_pages_into_chunks, create_vector_db, qa_prompt, invoke_doc_chain



def main_qa_chatbot(user_input, llm, url):
    # Initialize or retrieve chat history from session state
    chat_history = st.session_state.get("chat_history", ChatMessageHistory())

    # Initialize or retrieve AI model from session state
    chain = st.session_state.get("qa_model", None)
    if chain is None:
        chain = qa_prompt(llm)

    # Read and split the PDF document
    docs = read_pdf(url)
    chunks = split_pages_into_chunks(docs)

    # Retrieve relevant documents based on user's question
    retriever = create_vector_db(chunks)
    relevant_docs = retriever.invoke(user_input)

    # Get AI response
    response = invoke_doc_chain(relevant_docs, user_input, retriever, chain, chat_history)

    # Append the current user message and AI response to the chat history
    #chat_history.add_user_message(HumanMessage(content=user_input))
    chat_history.add_ai_message(AIMessage(content=response))

    # Display chat history
    for message in chat_history.messages:
        if isinstance(message, HumanMessage):
            st.write("You: " + message.content)
        elif isinstance(message, AIMessage):
            st.write("AI: " + message.content)

    # Store chat history and AI model in session state
    st.session_state["chat_history"] = chat_history
    st.session_state["qa_model"] = chain


# Set OpenAI API key as an environment variable

# Load environment variable from .env file
load_dotenv()

#Langsmith tracing
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

# access environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Get the directory path of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to the PDF file
url = os.path.join(current_directory, 'pdf_files', 'Claims_Flow.pdf')

# Open AI model to be used
llm = ChatOpenAI(temperature=0.5, max_tokens=1000)

# streamlit framework
st.title("ChatBot")
#st.subheader("Ask me about OHI")

user_input = st.text_area("You", key="user_input", value="")
button_clicked = st.button("Send")


if button_clicked :
    main_qa_chatbot(user_input, llm, url)
