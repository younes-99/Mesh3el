import streamlit as st
import sqlite3
import pandas as pd
import random 
import time
from openai import OpenAI


st.set_page_config(layout="wide")

st.title('Mesh3el Chatbot')

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


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



# response = f"Echo: {prompt}"
# Display assistant response in chat message container
with st.chat_message("assistant"):
      stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
      response = st.write_stream(stream)
st.session_state.messages.append({"role": "assistant", "content": response})