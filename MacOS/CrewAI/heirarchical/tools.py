from dotenv import load_dotenv
from crewai_tools import FileReadTool, BaseTool, SerperDevTool
import os

# Load environment variables
load_dotenv()

# Initialize the tool for internet searching capabilities
web_tool = SerperDevTool()

# Define FileReadTool
file_read_tool = FileReadTool()

# Define FileWriteTool (Custom Implementation)
class FileWriteTool(BaseTool):
    name: str = "FileWriteTool"
    description: str = "Tool to write content to a file."

    def _run(self, content: str, file_path: str) -> str:
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return f"Content written to {file_path}"
        except Exception as e:
            return str(e)

file_write_tool = FileWriteTool()
