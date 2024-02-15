import streamlit as st
import sqlite3
import pandas as pd

st.title('Mesh3el Chatbot')

st.chat_input('Type a message')

# Function to read data from SQLite database
def read_from_db():
    conn = sqlite3.connect('uploaded_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM uploaded_data")
    data = c.fetchall()
    conn.close()
    return data

st.write('Here is the data from the SQLite database:')
t = read_from_db()
st.dataframe(pd.DataFrame(t))