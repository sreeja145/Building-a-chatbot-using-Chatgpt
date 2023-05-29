import streamlit as st
from streamlit_chat import message

import os
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd

import json

with open('api json.json', 'r') as f:
    json_data = json.load(f)
    os.environ['OPENAI_API_KEY'] = json_data['API_KEY2']
    os.environ['SERPAPI_API_KEY'] = json_data['API_KEY']

# using session variables to store the chat history

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


def clear_text_input():
    global input_text
    input_text = ""


def get_text():
    global input_text
    input_text = st.text_input("Ask your question", key='input', on_change=clear_text_input)
    return input_text

def get_file(file_data):
    if '.csv' in file_data.name:
       df=pd.read_csv(file_data)
    else:
        df=pd.read_excel(file_data)
    return df

# creating a file uploader
uploaded_file = st.file_uploader("Choose a file")
user_input = get_text()
print(user_input)

if uploaded_file:
    dataframe=get_file(uploaded_file)
    agent=create_pandas_dataframe_agent(OpenAI(temperature=0),dataframe, verbose=True)

if st.button("Post"):
    with st.spinner("Waiting for the response..."):
        if user_input:
            output=agent.run(user_input)
            # storing the output
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state["generated"][i],key=str(i))
        message(st.session_state["past"][i],is_user=True,key=str(i)+'_user')



