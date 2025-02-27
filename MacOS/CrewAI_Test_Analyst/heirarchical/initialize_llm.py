import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        print(f"Error initializing LLM: {e}")
        return None

async def main():
    llm = await initialize_llm()
    if llm:
        print("LLM initialized successfully.")
    else:
        print("LLM initialization failed.")

if __name__ == "__main__":
    asyncio.run(main())