import sqlite3
import streamlit as st

# Function to create a connection to the SQLite database
def connect_db():
    conn = sqlite3.connect('healthcare_claims.db')
    return conn

# Function to retrieve and display data from the database
def display_table(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get the column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    conn.close()
    
    # Display the table in Streamlit
    if rows:
        st.write(f"### {table_name.capitalize()} Table")
        st.dataframe([dict(zip(columns, row)) for row in rows])
    else:
        st.write(f"No data available in {table_name} table.")

# Streamlit UI
st.title('Healthcare Claims Database Viewer')

# List of available tables
tables = ['members', 'providers', 'claims', 'procedures', 'diagnosis']

# Dropdown menu to select a table to display
selected_table = st.selectbox('Select a table to display:', tables)

# Button to display the selected table
if st.button('Display Table'):
    display_table(selected_table)