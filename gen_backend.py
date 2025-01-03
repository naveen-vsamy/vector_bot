import os
import boto3
import json
import time
from langchain.embeddings import BedrockEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
import streamlit as st

#Create the connection to Bedrock
bedrock_runtime = boto3.client(service_name='bedrock-runtime',
    region_name=st.secrets["AWS_DEFAULT_REGION"], aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"])

os.environ['PINECONE_API_KEY']=st.secrets["PINECONE_API_KEY"]
def similar_doc(prompt):
    index_name = "resume"

    embedding_model = BedrockEmbeddings(client=bedrock_runtime,model_id="amazon.titan-embed-text-v1" )
                    
    vectorstore = PineconeVectorStore(index_name=index_name, embedding = embedding_model)
    similar_search_results =  vectorstore.similarity_search(query = prompt, k = 3)
    return similar_search_results


from langchain import PromptTemplate

RAG_PROMPT_TEMPLATE = '''Here is some important context which can help inform the questions the Human asks.
Make sure to not make anything up to answer the question if it is not provided in the context.


{context}


Human: {human_input}

Assistant:
'''
PROMPT = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def create_response(human_input):
    prompt_data = PROMPT.format(human_input=human_input, context=similar_doc(human_input))
    inputText=prompt_data
    body_part=json.dumps({'inputText': inputText,
    'textGenerationConfig': {'maxTokenCount': 500,
    'stopSequences': [],
    'temperature': 0,
    'topP': 1}})
    response = bedrock_runtime.invoke_model(
        body=body_part,
        contentType="application/json",
        accept="application/json",
        modelId='amazon.titan-text-premier-v1:0'
    )

    response =  json.loads(response['body'].read())["results"][0]["outputText"]
    for word in response.split():
        yield word + " "
        time.sleep(0.2) 


