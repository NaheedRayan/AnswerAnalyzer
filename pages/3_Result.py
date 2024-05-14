import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os 
import numpy as np
import re 
pd.options.mode.chained_assignment = None  # default='warn'




# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')

def calculate_result(file_name):

    with st.spinner(f'Calculating {file_name}'):
        # print(file_name)
        student_df = pd.read_csv(f'student_doc_parsed/{file_name}')
        teacher_df = pd.read_csv(f'teacher_doc_parsed/teacher.csv')

        student_df['Received_mark'] = np.nan




        for i in range(len(student_df['Received_mark'])):
            teacher_question = teacher_df.iloc[i]['Question']
            teacher_answer = teacher_df.iloc[i]['Answer']
            teacher_mark = teacher_df.iloc[i]['Question_mark']

        
            student_answer = student_df.iloc[i]['Answer']
            student_mark = student_df.iloc[i]['Received_mark']




            # print(teacher_mark)
            

            prompt = f"""
                Behave Like a teacher. You will be given
                "TEACHER_QUESTION" :  The question teacher has asked
                "TEACHER_ANSWER" : The correct answer teacher has provided
                "TEACHER_MARK" : The value of the TEACHER_QUESTION

                "STUDENT_ANSWER" : The answer student wrote on TEACHER_QUESTION
                "RECEIVED_MARK" : The number teacher will give

                Now as a teacher what RECEIVED_MARK will you provide to your student by comparing your answer to students

                "TEACHER_QUESTION" : {teacher_question}
                "TEACHER_ANSWER" : {teacher_answer}
                "TEACHER_MARK" : {teacher_mark}

                "STUDENT_ANSWER" : {student_answer}
                "RECEIVED_MARK" :

                Note : TEACHER_MARK will be in number format and only print number

            """
            
            # response = model.generate_content(prompt , generation_config={'response_mime_type':'application/json'})
            response = model.generate_content(prompt)
            # Use findall method to extract all matches
            received_number = re.findall(r'\d+', response.text)
            student_df.at[i, 'Received_mark'] = int(received_number[0])
            print(f"{i} -- receieved number {received_number[0]}")
            # print(student_df)
            student_df.to_csv(f'student_result_doc/{file_name}', index=False)
            





    

# List all CSV files in the directory
csv_files_of_students = [f for f in os.listdir('student_doc_parsed') if f.endswith('.csv')]
csv_files_results = [f for f in os.listdir('student_result_doc') if f.endswith('.csv')]

st.write("### List of students doc")

# Display buttons to modify each CSV file
for file_name in csv_files_of_students:

    col1, col2 = st.columns([6, 4])

    with col1:
        st.write(f"{file_name}")
    
    with col2:
        if file_name in csv_files_results:
            st.write('Done')
        else:
            # for calculating student files
            if st.button(f"Calculate {file_name}"):
                calculate_result(file_name)
                st.rerun()


st.divider()
st.write('### Students score list')
csv_files_of_students_result = [f for f in os.listdir('student_result_doc') if f.endswith('.csv')]

def generate_grade(obtained_marks, total_marks):
    percentage = (obtained_marks / total_marks) * 100

    if percentage >= 90:
        grade = 'A+'
    elif percentage >= 80:
        grade = 'A'
    elif percentage >= 70:
        grade = 'B'
    elif percentage >= 60:
        grade = 'C'
    elif percentage >= 50:
        grade = 'D'
    else:
        grade = 'F'

    return grade

# Initialize an empty dictionary to store data
data = {
    'Name': [],
    'Scored': [],
    'Total': [],
    'Grade': []
}
df = pd.DataFrame(data)


for file_name in csv_files_of_students_result:
    student_df = pd.read_csv(f'student_result_doc/{file_name}')
    
    total_marks = 0
    obtained_marks = 0
    for i in range(len(student_df['Question_mark'])):
        received_number = re.findall(r'\d+', student_df.iloc[i]['Question_mark'])
        total_marks += int(received_number[0])
        # print(total_marks)


        obtained_number = student_df.at[i,'Received_mark']
        obtained_marks += obtained_number
        # print(obtained_marks)



    temp = {
        'Name': file_name,
        'Scored': obtained_marks ,
        'Total': total_marks,
        'Grade': generate_grade(obtained_marks,total_marks)
    }
    # print(df)
    df = df._append(temp , ignore_index =True)
    


    # st.write(f"{file_name} --- Scored  --- {obtained_marks}/{total_marks}")
sorted_df = df.sort_values(by='Scored',ascending=False)
st.write(sorted_df)
st.divider()

sorted_df.drop(columns=['Grade','Total'], inplace=True)

print(sorted_df)
# chart

st.bar_chart(sorted_df.set_index('Name') , color='#FF7E4B')