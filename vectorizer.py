'''
!pip install boto3
!pip install langchain_pinecone
!pip install langchain_aws
'''
import json
import boto3
import os
#from langchain_aws import BedrockEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone # Import Pinecone class
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from uuid import uuid4
def document_uploader(document):

    os.environ['PINECONE_API_KEY']= 'pcsk_CsMaa_A43NCBFZCg6hz2pwR7Tg2uXJpcckWveWq9FhnTExPSN41KmbEUQ3yXgsTcV9e4'
    os.environ['AWS_ACCESS_KEY_ID']= 'AKIA4AQ3T5MLKFVH3WNI'
    os.environ['AWS_SECRET_ACCESS_KEY']= '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'
    os.environ['AWS_DEFAULT_REGION']=  "us-east-1"

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
        chunk_size=3000,
        chunk_overlap=30,

    )
    split_docs = text_splitter.split_documents(docs)

    uuids = [str(uuid4()) for _ in range(len(split_docs))]

    vector_store.add_documents(documents=split_docs, ids=uuids)
    
    return True

