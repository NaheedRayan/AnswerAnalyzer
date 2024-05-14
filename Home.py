import streamlit as st
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
   

st.title("Answer Analyzer")
st.caption("Powered By Gemini Pro")


llm = ChatGoogleGenerativeAI(model="gemini-pro")




# input field
prompt = st.text_input("Ask a Question")





if prompt:


    result = llm.invoke(prompt)
    print(result.content)

   
    

    # outputing the response
    st.write(result.content)