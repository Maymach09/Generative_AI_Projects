from dotenv import load_dotenv
from crewai_tools import SerperDevTool, FileReadTool
import os


load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

# Initialize the tool for internet searching capabilities
web_tool = SerperDevTool()
file_tool = FileReadTool()