import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import sqlite3

st.set_page_config(layout="wide")

st.title("Upload CSV file")

# Function to create SQLite database and table
def create_sqlite_db(df):

    conn = sqlite3.connect('uploaded_data.db')
    c = conn.cursor()

    # Infer column names and data types from the DataFrame
    columns_str = ", ".join([f"{col} TEXT" for col in df.columns])
    c.execute(f"CREATE TABLE IF NOT EXISTS uploaded_data ({columns_str})")

    conn.commit()
    conn.close()

# Function to insert data from CSV into SQLite database
def insert_into_db(df):
    
    conn = sqlite3.connect('uploaded_data.db')
    df.to_sql('uploaded_data', conn, if_exists='replace', index=False)
    conn.close()

# Function to read data from SQLite database
def read_from_db():
    conn = sqlite3.connect('uploaded_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM uploaded_data")
    data = c.fetchall()
    conn.close()
    return data


@st.cache_data
def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# File uploader
uploaded_file = st.file_uploader('Upload a CSV file')
add_to_database = st.checkbox('Save to database for later analysis')


if uploaded_file is not None:

    # Read CSV file
    df = read_csv(uploaded_file)
    if add_to_database:
        # Creating SQLite database and table
        create_sqlite_db(df)
        insert_into_db(df)

    # Display preview of the CSV file
    st.subheader("Preview of CSV File")
    st.write(df)

try:
    st.write('Here is the data from the SQLite database:')
    t = read_from_db()
    st.write(pd.DataFrame(t))

except:
    pass

