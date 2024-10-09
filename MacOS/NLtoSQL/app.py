import sqlite3
import pandas as pd
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

# Function to create a connection to the SQLite database
def connect_db():
    conn = sqlite3.connect('healthcare_claims.db')
    return conn

# Function to execute the SQL query and return the results as a pandas DataFrame
def execute_sql(query):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # Fetch column names to display them in the DataFrame
    columns = [description[0] for description in cursor.description]
    conn.close()

    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(result, columns=columns)
    return df

# Function to call OpenAI API and convert natural language to SQL
def generate_sql(user_query):
    prompt = f"""
    Convert the natural language query mentioned below into a SQL query for a database containing members, providers, claims, diagnosis and procedures tables

    columns in members table: id, name, age, gender, insurance_id
    columns in providers table: id, name, specialty, hospital
    columns in claims table: id, member_id, provider_id, claim_date, amount, status
    columns in diagnosis table: id, claim_id, treatment_name, cost
    columns in procedures table: id, claim_id, diagnosis_code, description


    Query: "{user_query}"
    
    SQL query:
    """

    # Using the new OpenAI ChatCompletion structure
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    sql_query = response.choices[0].message.content.strip()
    return sql_query

# Streamlit UI
st.title('Natural Language to SQL App')

# Input: User query
user_query = st.text_input("Write text to convert to SQL")

# Button to submit the query
if st.button("Generate SQL and Execute"):
    if user_query:
        with st.spinner("Generating SQL..."):
            # Step 1: Convert natural language query to SQL
            sql_query = generate_sql(user_query)
            st.write(f"Generated SQL Query: `{sql_query}`")

            # Step 2: Execute the SQL query and display the results
            with st.spinner("Executing SQL..."):
                try:
                    results_df = execute_sql(sql_query)
                    if not results_df.empty:
                        st.write("Results:")
                        st.dataframe(results_df)  # Display the results in a table format
                    else:
                        st.write("No results found.")
                except Exception as e:
                    st.error(f"Error executing SQL: {e}")
    else:
        st.error("Please enter a query.")