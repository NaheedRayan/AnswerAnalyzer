import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pdf2image import convert_from_bytes
import json

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# Directory to save the images
output_directory = 'student_doc_pic'


# initiating the model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


# function for cleaning data in a directory
def remove_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)


st.write('### Actual Q&A from the Teacher')

df = pd.read_csv('teacher_doc_parsed/teacher.csv')
st.dataframe(df)
st.divider()



st.write('### Upload file')
# file uploader
uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)







for uploaded_file in uploaded_files:

    # Initialize an empty dictionary to store data
    data = {
        'Question_name': [],
        'Question': [],
        'Answer': [],
        'Question_mark': []
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
# if the file is present
    if uploaded_file is not None:

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0.0, text=progress_text)

        # Store Pdf with convert_from_path function
        images = convert_from_bytes(uploaded_file.getvalue())

        # dict for saving the file name and url from FILE API
        sample_file_data = {}
        for i in range(len(images)):
            images[i].save(f"{output_directory}/page_{i}.jpg", 'JPEG')

            # uploading the image in FILE API 
            sample_file = genai.upload_file(path=f"{output_directory}/page_{i}.jpg", display_name=f"page_{i}.jpg")
            sample_file_data[sample_file.name] = sample_file.uri

            print(f"Uploaded file 'page_{i}.jpg' -- '{sample_file.name}' as: {sample_file.uri}")
            # st.write(f"Uploaded file 'page_{i}.jpg' -- '{sample_file.name}' as: {sample_file.uri}")
            # st.write(f"page_{i} uploaded and is being parsed")

            my_bar.progress( i/len(images) , text=f"Parsing Page {i}/{len(images)}")





            # response = model.generate_content(['''Just only do OCR and show the output in appropriate python obj format 
            #                                  {
            #                                     Question_name : "Question01"
            #                                     Question : "What is a cat"
            #                                     Answer : "A cat is an animal"
            #                                     Question_mark : "10"
            #                                  }
            #                                  ''', sample_file] ,  generation_config={'response_mime_type':'application/json'})


            response = model.generate_content(['''Just only do OCR and show the output using the following schema:

            {"data": list[QUESTION]}

            QUESTION = {"Question_name": str, "Question": str, "Answer": str, "Question_mark": str}

            All fields are required.

            Important: Only return a single piece of valid JSON text.
            ''', sample_file] ,  generation_config={'response_mime_type':'application/json'}) 



            # print(type(response.text))
            json_obj = (json.loads(response.text))
            # print(type(json_obj))

            for dict in json_obj['data']:
                # Append dictionary to DataFrame
                # print(type(dict))
                df = df._append(dict, ignore_index=True)

            # print(parser.get_format_instructions())

            # st.write(response.text)
            # print(response.text)


            genai.delete_file(sample_file.name)
            print(f'Deleted page_{i}.jpg -- {sample_file.name}.')


        my_bar.progress( 1.0 , text="Done")

        print(df)
        # Save DataFrame to CSV
        df.to_csv(f'student_doc_parsed/{uploaded_file.name}.csv', index=False)
        #editable dataframe 
        # edited_df = st.data_editor(df)

        # for key, value in sample_file_data.items():
        #     print(key, value)


        # clearing everything
        sample_file_data.clear
        remove_files_in_directory('student_doc_pic')





directory = 'student_doc_parsed'

def list_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    return csv_files

if directory:
    if os.path.isdir(directory):
        st.write('### List of uploaded files')
        csv_files = list_csv_files(directory)

        st.dataframe(csv_files)
        # for csv_file in csv_files:
        #     st.write(csv_file)
    else:
        st.write('Invalid directory path')








