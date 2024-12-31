#pip install streamlit
import streamlit as st
import boto3
import langchain
import gen_backend as gb
import vectorizer
import time

with st.sidebar:
    st.title("Upload your PDF file here")
    st.markdown("Please don't upload password protected pdf's or documents with sensitive personal information.")
    file2 = st.file_uploader(label = "Select your .pdf document")
    
    if file2 != None :
            #function to read data and upload to vector db
           # st.write("Document uploaded. Now you can ask questions related to your document to the chatbot")

        if st.button(label = "upload pdf", type = "primary") :
                #function to read data and upload to vector db
                vectorizer.pdf_uploader(file2)
                st.write("PDF document uploaded. Refresh the page once, then you can ask questions related to your document to the chatbot")

st.title("PDF Assistant bot")
st.makdown("Please enter your queries with in proper wordings. Try to ask questions with clear information. This bot doesn't remember earlier questions, so each query's response depends on the indivudal query and data from the document alone.")

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
