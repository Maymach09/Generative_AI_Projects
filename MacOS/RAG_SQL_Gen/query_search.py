from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
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
print(openai_api_key)

CHROMA_PATH = "/Users/maymach09/Documents/GenAI09/MacOS/RAG_SQL_Gen/chromaDB"


PROMPT_TEMPLATE = """

----------------------------------------------------------------------------------------------------------------------------------------------------------
User Prompt for Generating SQL:
----------------------------------------------------------------------------------------------------------------------------------------------------------

You are a database expert who's job is to generate accurate and optimized SQL queries based on the database schema and natural language request provided below. 

Database Schema:
{context}

User Query:
{scenario}

Instructions:

	1.	Understand the Database Schema:
        The schema information will be provided in chunks retrieved from a vector database. Each chunk contains details about tables, columns, and \
        relationships such as primary keys and foreign keys. Carefully review this information to determine how to structure the query.
	2.	Process the Request:
        Based on the natural language request and the schema details provided, generate a valid SQL query. Ensure you:
        •	Identify the relevant tables and columns.
        •	Include JOINs if there are relationships between tables.
        •	Use WHERE, GROUP BY, HAVING, and ORDER BY clauses as needed for filtering, aggregating, and sorting.
        •	Handle any specified conditions, such as date ranges, customer filters, etc.
	3.	Optimization:
        •	Use appropriate indices (such as those on primary and foreign keys) to optimize query performance.
        •	Use aliases to improve the readability of complex queries.
        •	Ensure the query is efficient, especially for large datasets or complex relationships.
	4.	Output Format:
        Return the SQL query in a code block formatted using triple backticks (```).

Examples:

Example 1:

    Request:
    “Show the total number of orders placed by each customer, along with their first and last names.”

    Relevant Schema Details:

        •	Table customers (columns: customer_id, first_name, last_name)
        •	Table orders (columns: order_id, customer_id, order_date)

    Generated SQL Query:
    SELECT c.first_name, c.last_name, COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name;

Example 2:

    Request:
    “List the names of all products in the 'Furniture' category, along with their prices.”

    Relevant Schema Details:

        •	Table products (columns: product_id, product_name, category_id, price)
        •	Table categories (columns: category_id, category_name)

    Generated SQL Query:
    SELECT p.product_name, p.price
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    WHERE c.category_name = 'Furniture';

----------------------------------------------------------------------------------------------------------
Generate the SQL following the instructions provided.
----------------------------------------------------------------------------------------------------------

"""

def main():
    
    # streamlit framework
    st.title("AI Tester")
    topic = st.text_area("Ask a question:")
    

    if topic:
        try:
            # Prepare the  DB
            embedding = OpenAIEmbeddings()
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
           
           # Search the DB.
            results = db.similarity_search_with_relevance_scores(topic, k=2)
            if len(results) == 0 or (len(results[0]) > 1 and results[0][1] < 0.6):
                st.write("Unable to find matching results.")
                return
            else:
                st.write(results)
            #Prepare prompt
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(context=context_text, scenario=topic)
            st.write(prompt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        model = ChatOpenAI(api_key=openai_api_key, temperature=0.7)
        response_text = model.predict(prompt)
        
        sources = [f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})" for doc, _score in results]

        #print document source
        st.write(f"\nSource Document: \n\n{sources}")

        # print output SQL
        st.text_area("Response", value=response_text, height=400)

if __name__ == "__main__":
    main()