import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAI



# import module
from pdf2image import convert_from_bytes

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# Directory to save the images
output_directory = 'teacher_doc_pic'

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

def remove_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)



uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False)



if uploaded_file is not None:

    # Store Pdf with convert_from_path function
    images = convert_from_bytes(uploaded_file.getvalue())

    sample_file_data = dict()
    for i in range(len(images)):
        images[i].save(f"{output_directory}/page_{i}.jpg", 'JPEG')
        
        # uploading the image in FILE API 
        sample_file = genai.upload_file(path=f"{output_directory}/page_{i}.jpg", display_name=f"page_{i}.jpg")
        sample_file_data[sample_file.display_name] = sample_file.uri

        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        st.write(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        response = model.generate_content(['''Just only do OCR and show the output in the following json format
                                         {
                                            Question_num : "Question01"
                                            Question : "What is a cat"
                                            Answer : "A cat is an animal"
                                            Question_mark : "10"
                                         }
                                         ''', sample_file])
        
        st.write(response.text)
        print(response.text)

        genai.delete_file(sample_file.name)
        print(f'Deleted {sample_file.display_name}.')


    remove_files_in_directory('teacher_doc_pic')
    
    for key, value in sample_file_data.items():
        print(key, value)

    sample_file_data.clear
    
    

    # for i, image in enumerate(images):
    #     st.image(image, caption=f"Page {i+1}", use_column_width=True)



    # print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")


