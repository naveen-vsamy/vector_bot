#pip install streamlit
import streamlit as st
import boto3
import langchain
import gen_backend as gb
import vectorizer
import time

with st.sidebar:
    st.title("Private Document")
   
    file = st.file_uploader(label = "Select your text document")
    
    if file != None :
            #function to read data and upload to vector db
           # st.write("Document uploaded. Now you can ask questions related to your document to the chatbot")

        if st.button(label = "upload", type = "primary") :
                #function to read data and upload to vector db
                vectorizer.document_uploader(file)
                st.write("Document uploaded. Now you can ask questions related to your document to the chatbot")


st.title("Assistant bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role" : "user", "content" : prompt})

    with st.chat_message("assistant"):
        
        response = st.write_stream(gb.create_response(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})
