from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from typing import Dict
import sqlite3


# This is a sub-function to read the pdf file -------Sub-Function #1.1
def read_pdf(pdf_url):
    try:
        # Read PDF using PyPDF2
        loader = PyPDFLoader(pdf_url)
        pages = loader.load()
        return pages
    except Exception as e:
        return {"error": f"Error reading PDF: {e}"}
    
# This is a sub-function to split the text -------Sub-Function #1.2
def split_pages_into_chunks(pages):
    doc_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 200,
    )
    split_pages = doc_splitter.split_documents(pages)
    return split_pages

#Function to define vectordb -------Sub-Function #2.1
def create_vector_db(document_chunks):
    #Initialize OpenAI embedding
    embeddings = OpenAIEmbeddings()
    # Create vector db to store raw documents
    vectordb = Chroma.from_documents(
        documents=document_chunks,
        embedding=embeddings,
    )
    
    # Retrieve relevant chunks and store them in a variable
    retriever = vectordb.as_retriever(k=3)
    return retriever

# Function to set up the prompt -------Sub-Function #3.1
def qa_prompt(model):

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                '''
                You are a Software Testing knowledge assistant.
                You should answer user's questions based on the context below delimited by triple backticks.
                ```{context}```                

                Refer the below given sample_conversation to construct the response:
                user: What is boundary value analysis?
                assistant: 1. Boundary Value Analysis (BVA) is a software testing technique that focuses on testing the boundary values of input parameters.\n 
                           2. It involves testing values at the boundaries of valid and invalid partitions to identify potential defects.\n
                           3. BVA helps ensure that the system handles boundary values correctly, as these values are more likely to cause errors.
                user: What is functional testing?
                assistant: 1. Functional testing is a type of testing that evaluates the functions and behaviors of a software system.
                           2. Functional testing is performed to ensure that functionality of the application meets the specified requirements.
                user: What is the Capital of USA?
                assistant: Since, the question is not related to Software testing, I cannot answer that.
                user: What is Acne?
                assistant: Since, the question is not related to Software testing, I cannot answer that.

                If the question is unrelated to the context do not answer and say "Since, the question is not \
                related to Software testing, I cannot answer that.

                ''',
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return create_stuff_documents_chain(model, question_answering_prompt)
    

# Function to invoke document chain with raw documents -------Sub-Function #3.2

def invoke_doc_chain(docs, question, retriever, chain, chat_history):
    if not chat_history:
        # Initialize ChatMessageHistory if not provided
        chat_history = ChatMessageHistory()
    
    # Add user message
    chat_history.add_user_message(HumanMessage(content=question))


    chain.invoke(
        {
            # Pass messages from chat history
            "messages": chat_history.messages,
            "context": docs,
        }
    )

    retrieval_chain = RunnablePassthrough.assign(
        context=parse_retriever_input | retriever,
        ).assign(
        answer=chain,
    )

    chat_history = retrieval_chain.invoke(
        {
            "messages": chat_history.messages,
        }
    )

    return chat_history.get("answer", "")

# To retrieve and save last chat message -------Sub-Function #3.2.1
def parse_retriever_input(params: Dict):
    return params["messages"][-1].content
