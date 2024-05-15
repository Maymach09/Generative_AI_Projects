import os
import traceback
import json
import streamlit as st
from dotenv import load_dotenv
from src.tcgenerator.utils import read_file, output_dataframe, output_file
from src.tcgenerator.logger import logging
from src.tcgenerator.TC_TM_Generator import combined_chain
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv

#Langsmith
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

# Main function
def main():
    st.title("Requirements Processing")
    
    # Upload button
    uploaded_file = st.file_uploader("Upload File", type=['txt', 'pdf'])
    language = st.text_input("Enter the programming language for automated tests")
    button = st.button("Generate")
    # req_button = st.button("Generate Requirements")
    # tc_button = st.button("Generate Test Cases")
    # tm_button = st.button("Generate TM")
    # code_button = st.button("Generate Code")


    if button:
        with st.spinner('Processing...'):
            try:
                # read file and store content in a variable
                text = read_file(uploaded_file)

                # count tokens and cost of openAPI call
                with get_openai_callback() as cb:
                    response = combined_chain(
                        {
                        "requirements": text,
                        "summary_json_format": json.dumps(summary_json_format),
                        "tc_json_format": json.dumps(tc_json_format),
                        "tm_json_format": json.dumps(tm_json_format),
                        "code_template": json.dumps(code_format),
                        "programming_language" : json.dumps(language) 
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error: {}".format(str(e)))
            else:
                st.success("Execution completed successfully!")
                st.write("Count of tokens used to make OpenAI API calls:\n")
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    # Extract response and save output files
                    finalized_requirements = response.get("summarized_requirements")
                    output_file(finalized_requirements, output_folder, output_file_name="requirements.txt")
                    req_df = output_dataframe(finalized_requirements)
                    output_file(req_df, output_folder, output_file_name="requirements.csv")

                    finalized_test_cases = response.get("test_cases")
                    output_file(finalized_test_cases, output_folder, output_file_name="test_cases.txt")
                    tc_df = output_dataframe(finalized_test_cases)
                    output_file(tc_df, output_folder, output_file_name="test_cases.csv")

                    finalized_traceability_matrix = response.get("traceability_matrix")
                    output_file(finalized_traceability_matrix, output_folder, output_file_name="traceability_matrix.txt")
                    tm_df = output_dataframe(finalized_traceability_matrix)
                    output_file(tm_df, output_folder, output_file_name="traceability_matrix.csv")

                    finalized_code = response.get("code")
                    output_file(finalized_code, output_folder, output_file_name="automated_tests.txt")
                    


# load requirement's json format
with open('C:\\Documents\\AI\\GenAI\\E2E Test Case generator\\req_response.json','r') as req_file:
    summary_json_format= json.load(req_file)

# load test case's json format
with open('C:\\Documents\\AI\\GenAI\\E2E Test Case generator\\tc_response.json','r') as tc_file:
    tc_json_format= json.load(tc_file)

# load traceability matrix's json format
with open('C:\\Documents\\AI\\GenAI\\E2E Test Case generator\\tm_response.json','r') as tm_file:
    tm_json_format= json.load(tm_file)

# load code format
with open('C:\\Documents\\AI\\GenAI\\E2E Test Case generator\\code_template.txt','r') as code_file:
    #code_format= json.load(code_file)
    code_format = code_file.read()

output_folder = "C:\\Documents\\AI\\GenAI\\E2E Test Case generator\\Test Data\\Output Files\\"

if __name__ == "__main__":
    main()