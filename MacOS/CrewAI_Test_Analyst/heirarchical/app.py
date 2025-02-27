import streamlit as st
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tools import pdf_read_tool

# Load environment variables
load_dotenv()

# Asynchronous initialization of llm
async def initialize_llm():
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing LLM: {e}")
        return None

# Main function to run Streamlit app
async def main():
    # Initialize llm asynchronously
    llm = await initialize_llm()
    if llm:
        st.success("LLM initialized successfully.")
        # Streamlit UI code
        st.title("Generate Test Cases from Business Requirement Document (BRD)")

        # File upload section
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

        if uploaded_file is not None:
            st.subheader("Content of the uploaded PDF:")
            brd_content = pdf_read_tool._run(uploaded_file)
            st.write(brd_content)

            # Button to generate test cases
            if st.button("Generate Test Cases"):
                st.info("Generating test cases...")
                # Use llm to generate test cases
                generated_cases = llm.submit_prompt(brd_content)
                st.success("Test cases generated successfully:")
                st.write(generated_cases)

    else:
        st.error("LLM initialization failed.")

if __name__ == "__main__":
    asyncio.run(main())