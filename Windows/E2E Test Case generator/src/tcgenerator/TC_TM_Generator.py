from dotenv import load_dotenv
from src.tcgenerator.utils import read_file
from src.tcgenerator.logger import logging
import os

# required libraries from langchain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

# Load environment variable from .env file
load_dotenv()

#Langsmith
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

#langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

# access environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# create an llm object
llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.5)


# prompt to summarize the requirements
summarize_template = """
As a product owner, your responsibility is to distill the provided requirements into a concise and comprehensive summary. \
Your task is to generate appropriate requirements based on the {requirements}, ensuring that all aspects mentioned in the \
requirements are adequately covered.

Generate as many requirements as necessary to encapsulate the specified functionality, ensuring that each aspect is \
addressed without duplication. Avoid adding any additional information beyond what is provided in the original requirements.

Finally, format your response according to the provided summary_json_format given below and use it as a guide.
{summary_json_format}
"""

# contruct input prompt for summarizing the requirements
summarize_prompt = PromptTemplate(
    input_variables=["requirements","summary_response_json"],
    template=summarize_template
)

# create a chain to get summarized requirements as output
summary_chain = LLMChain(
    llm = llm,
    prompt = summarize_prompt,
    output_key = "summarized_requirements",
    verbose = True
)

# prompt to create test cases
tc_generation_template = """
As an experienced software tester, your task is to create comprehensive test cases based on the provided \
user requirements. Utilize industry-standard testing techniques such as Boundary Value Analysis, \
Equivalence Partitioning, Decision Table Testing, and Use Case Testing to ensure thorough coverage of both positive \
and negative scenarios.

Generate 5 test cases for each requirement listed in {summarized_requirements}, that validates the functionality under various conditions. 
for e.g., if there are 10 requirements in the {summarized_requirements} then you need to create 50 test cases i.e. 5 for each.
Remember to also cover edge cases and error handling to maximize test coverage.

Finally, format your response according to the tc_json_format template provided below and use it as a guide.
{tc_json_format}

Now, proceed with the test case generation, considering the above instructions.

"""

# contruct input prompt to create test cases
tc_generation_prompt = PromptTemplate(
    input_variables=["tc_json_format", "summarized_requirements"],
    template=tc_generation_template,
)


# create a chain to get test cases as output
tc_chain = LLMChain(
    llm = llm,
    prompt = tc_generation_prompt,
    output_key = "test_cases",
    verbose = True
)


# prompt to create test cases
tm_generation_template = """
Your role as a software tester entails the creation of a traceability matrix to establish clear links between user \
requirements and the corresponding test cases. This matrix serves as a crucial document for ensuring comprehensive \
test coverage and validating that all requirements are adequately addressed.

To construct the traceability matrix, meticulously match each user requirement listed in {summarized_requirements} \
to the relevant test case names listed in {test_cases}. If a single requirement is covered by multiple test cases, \
generate a distinct entry for each test case to maintain granularity.

Lastly, organize your response according to the specified tm_json_format template provided below. Do not add any additional character on your own.
Ensure that the resulting matrix accurately reflects the relationships between requirements and test cases. 

{tm_json_format}
"""

# contruct input prompt to create traceability matrix
tm_generation_prompt = PromptTemplate(
    input_variables=["summarized_requirements", "test_cases", "tm_json_format"],
    template=tm_generation_template,
)

# create a chain to get traceability matrix as output
tm_chain = LLMChain(
    llm = llm,
    prompt = tm_generation_prompt,
    output_key = "traceability_matrix",
    verbose = True
)

# prompt to create automated tests in python
code_generation_template = """
You are a Software Developer. Your job is to write unit test code for the {test_cases} in python.
To write the code take each test case, and write the code based on the steps defined.
Also, ensure to add the comments in the code wherever necessary.

Provide the output in the format given below.
{code_template}


"""

# contruct input prompt to create traceability matrix
code_generation_prompt = PromptTemplate(
    input_variables=["test_cases", "programming_language", "code_template"],
    template=code_generation_template,
)

# create a chain to get traceability matrix as output
code_chain = LLMChain(
    llm = llm,
    prompt = code_generation_prompt,
    output_key = "code",
    verbose = True
)

# combine all the four chains created above
combined_chain = SequentialChain(
    chains= [summary_chain, tc_chain, tm_chain, code_chain],
    input_variables= ["requirements","summary_json_format", "tc_json_format", "tm_json_format","programming_language", "code_template"],
    output_variables= ["summarized_requirements", "test_cases", "traceability_matrix", "code"],
    verbose = True
)
