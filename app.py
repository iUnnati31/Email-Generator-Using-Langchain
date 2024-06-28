import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

# Function to get response from local Ollama model
def getResponse(input_text, email_subject, email_recipient, email_style):
    llm = ChatGroq(groq_api_key=groq_api_key,
                   model_name="Llama3-8b-8192")
    
    # Prompt Template
    template = """
        Write a {email_style} email with the subject "{email_subject}" to {email_recipient}. The content of the email should be about "{input_text}".
    """
    
    prompt = PromptTemplate(input_variables=["email_subject", "email_recipient", "input_text", "email_style"],
                            template=template)
    
    # Generate the response from the local Ollama model
    formatted_prompt = prompt.format(email_subject=email_subject, email_recipient=email_recipient, input_text=input_text, email_style=email_style)
    response = llm.invoke(formatted_prompt)
    response_text = str(response)
    return response_text

# Streamlit interface
st.set_page_config(page_title="Generate Emails", page_icon='📧', layout='wide', initial_sidebar_state='collapsed')

st.header("Generate Emails 📧")

input_text = st.text_input("Enter the Email Content")

# Creating fields for additional inputs
col1, col2 = st.columns([5, 5])

with col1:
    email_subject = st.text_input('Email Subject')
with col2:
    email_recipient = st.text_input('Email Recipient')

# Add a select box for email style (formal or informal)
email_style = st.selectbox("Select Email Style", ["Formal", "Informal"])

submit = st.button("Generate")

# Final response
if submit:
    response = getResponse(input_text, email_subject, email_recipient, email_style)

    st.write(response.replace("\n", "  \n"))
