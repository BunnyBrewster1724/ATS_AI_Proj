import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    # Initialize the model with the correct version (if this is the version you want)
    model = genai.GenerativeModel('gemini-1.5-flash')  # Set the model version when initializing
    
    # Call the generate_content method without passing 'model' as an argument
    response = model.generate_content(contents=[input, pdf_content[0], prompt])
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        #convert to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format='JPEG')
        image_byte_arr = image_byte_arr.getvalue()
        
        pdf_parts =[
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()  #encode to base64
            }
        ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("File not found")


# Streamlit App 
st.set_page_config(page_title="ATS Resume Check", page_icon=":book:")
st.header("ATS Tracking system")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully!! ")
    
submit1 = st.button("Tell me About the resume")
submit2 = st.button("How can I improve my skills? ")
submit3 = st.button("Percentage match")
submit4 = st.button("Score Check")  # New button for ATS score check

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt2 = """
 You are an Technical human resource manager with expertise in data science,
 your role is to scrutinize the resume in light of the job description provided. 
 Share your insights on the candidates suitability for the role from an HR perspective. 
 Additionally, offer advice on enhancing the candidates skills and identify areas with improvement. """
 
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, web development, big data engineering,
 data analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt4 = """
You are an advanced ATS (Applicant Tracking System) analyzer specializing in resume evaluation. 
Assess this resume against the job description and provide:
1. An overall ATS score out of 100
2. A breakdown of the score by these categories:
   - Keyword match (0-25): How well the resume contains job-specific keywords
   - Skills relevance (0-25): Alignment of candidate's skills with required skills
   - Experience match (0-25): How well the experience matches job requirements
   - Education & certifications (0-25): Relevance of qualifications to the position
3. List of suggested improvements to increase the ATS score
4. Format your response clearly with section headers and make it visually scannable
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:  # New condition for ATS score check button
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("ATS Score Analysis")
        st.write(response)
    else:
        st.write("Please upload the resume")