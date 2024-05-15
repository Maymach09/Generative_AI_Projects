from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st
import json

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
openai_api_key = os.environ.get('OPENAI_API_KEY')

CHROMA_PATH = "chroma"
tc_format_path = "/Users/maymach09/Documents/GenAI/macbook/GenAI/RAG_TestCases/tc_json_format"

# Load the JSON format from the separate file
with open(tc_format_path, "r") as json_file:
    tc_json_format = json.load(json_file)

# Convert the JSON format to a string
tc_format_str = json.dumps(tc_json_format, indent=4)


PROMPT_TEMPLATE = """
You are a software tester. Your job is to write analyze the context given below which is delimited by triple backticks and write the test cases based on them.
Write at least 10 test cases and make sure to include positive as well as negative test cases.
Use various industry standard test case techniques such as boundary value analsys, equivalence partitioning,Decision Table Testing, Use Case Testing etc.

```{context}```

Finally, format your response according to the output_format provided below and use it as a guide.
{output_format}

"""

def main():
    
    # streamlit framework
    st.title("AI Tester")
    query = st.text_area("Ask a question:")
    

    if query:
        try:
            # Prepare the  DB
            embedding = OpenAIEmbeddings()
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
           
           # Search the DB.
            results = db.similarity_search_with_relevance_scores(query, k=2)
            if len(results) == 0 or results[0][1] < 0.6:
                st.write(f"Unable to find matching results.")
                return
            else:
                st.write(results)
            #Prepare prompt
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, scenario=query, output_format=tc_format_str)
            st.write(prompt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        model = ChatOpenAI(api_key=openai_api_key, temperature=0.7)
        response_text = model.predict(prompt)

        # Assuming response_text contains the JSON string
        response_data = json.loads(response_text)

        # Convert the response data back to a JSON-formatted string with indentation
        formatted_json = json.dumps(response_data, indent=4)

        sources = [f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})" for doc, _score in results]
        
        formatted_response = f"Response: {formatted_json}"
        
        #print document soource
        st.write(f"\nSource Document: \n\n{sources}")

        # print output test cases
        st.text_area("Formatted Response", value=formatted_response, height=400)

if __name__ == "__main__":
    main()