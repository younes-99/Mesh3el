import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")

st.title('Mesh3el Chatbot')


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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

response = f"Echo: {prompt}"
# Display assistant response in chat message container
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})