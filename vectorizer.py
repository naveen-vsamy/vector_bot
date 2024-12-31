import json
import boto3
import os
from langchain_aws import BedrockEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone # Import Pinecone class
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader
from uuid import uuid4
import streamlit as st

os.environ['PINECONE_API_KEY']= st.secrets["PINECONE_API_KEY"]
os.environ['AWS_ACCESS_KEY_ID']= st.secrets["AWS_ACCESS_KEY_ID"]
os.environ['AWS_SECRET_ACCESS_KEY']= st.secrets["AWS_SECRET_ACCESS_KEY"]
os.environ['AWS_DEFAULT_REGION']=  st.secrets["AWS_DEFAULT_REGION"]


'''
def document_uploader(document):

    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

    # Create a Pinecone client instance
    pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"], environment="us-east-1")

    # Get the index using the Pinecone client instance
    index = pinecone_client.Index("resume")

    # Initialize PineconeVectorStore with the index and embeddings
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    # create a loader
    docs = []
    # loader = TextLoader('')
    docs.append(Document(page_content=document))

    # split documents into chunks
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=500,
        chunk_overlap=40,

    )
    split_docs = text_splitter.split_documents(docs)

    uuids = [str(uuid4()) for _ in range(len(split_docs))]

    vector_store.add_documents(documents=split_docs, ids=uuids)
    
    return True
'''
def pdf_uploader(file):

    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

    # Create a Pinecone client instance
    pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"], environment="us-east-1")

    # Get the index using the Pinecone client instance
    index = pinecone_client.Index("resume")

    # Initialize PineconeVectorStore with the index and embeddings
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    # create a loader
    file = PdfReader(file)
    docs = []
    doc = file.pages[0].extract_text()
    l = len(file.pages)
    
    for i in range(0,len(file.pages)):
        doc=file.pages[i].extract_text()
        docs.append(Document(page_content = doc))

    # split documents into chunks
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=3000,
        chunk_overlap=300,

    )
    split_docs = text_splitter.split_documents(docs)

    uuids = [str(uuid4()) for _ in range(len(split_docs))]

    vector_store.add_documents(documents=split_docs, ids=uuids)
    
    return True