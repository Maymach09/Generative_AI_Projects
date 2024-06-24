from dotenv import load_dotenv
from crewai_tools import BaseTool, SerperDevTool
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# Call the gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

#API key for web search
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Initialize the tool for internet searching capabilities
web_tool = SerperDevTool()

#Tool to read input from a file
class ReadBRDTool(BaseTool):
    name: str = "Read BRD Tool"
    description: str = "Reads the content of the Business Requirement Document (BRD)."

    def _run(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
txt_read_tool = ReadBRDTool()

#Tool to write output to a file
class FileWriteTool(BaseTool):
    name: str = "File Write Tool"
    description: str = "Writes content to a specified file."

    def _run(self, content: str, file_path: str) -> str:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content written to {file_path}"

file_write_tool = FileWriteTool()

#Read PDF document

class ReadPDFTool(BaseTool):
    name: str = "Read BRD Tool"
    description: str = "Reads the content of the Business Requirement Document (BRD)."

    def _run(self, file_path: str) -> str:
        content = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page in range(num_pages):
                page_content = reader.pages[page].extract_text()
                content += page_content
        return content
    
pdf_read_tool = ReadPDFTool()