import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API Key is missing! Ensure it is set in the .env file.")
