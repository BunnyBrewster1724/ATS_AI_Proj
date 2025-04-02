import base64
import io
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

# This must be the first Streamlit command
st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📝", layout="wide")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    # Initialize the model with the correct version
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Call the generate_content method
    response = model.generate_content(contents=[input, pdf_content[0], prompt])
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        pdf_bytes = uploaded_file.read()
        
        # Open the PDF using PyMuPDF
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Get the first page
        first_page = pdf_document.load_page(0)
        
        # Render the page to an image
        pix = first_page.get_pixmap()
        
        # Convert to bytes
        image_byte_arr = pix.tobytes("jpeg")
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()
            }
        ]
        
        pdf_document.close()
        return pdf_parts
    else:
        raise FileNotFoundError("File not found")

# Custom CSS for better UI - moved after set_page_config
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        font-weight: bold;
        margin-top: 2rem;
    }
    .info-text {
        font-size: 1rem;
        color: #424242;
    }
    .highlight {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0D47A1;
    }
    .upload-section {
        border: 2px dashed #1E88E5;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #E3F2FD;
    }
    .results-section {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
        border-left: 5px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">ATS Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="info-text">Optimize your resume for Applicant Tracking Systems with AI-powered analysis</div>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("### Job Description")
    st.markdown("Paste the job description you're applying for:", unsafe_allow_html=True)
    input_text = st.text_area("Job Description", height=200, key="input", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.success("✅ Resume uploaded successfully!")
        try:
            # Use PyMuPDF for preview
            pdf_bytes = uploaded_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            first_page = pdf_document.load_page(0)
            pix = first_page.get_pixmap()
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image for display
            img = Image.open(io.BytesIO(img_data))
            
            # Display the image
            st.image(img, width=250, caption="Resume Preview")
            
            # Reset file pointer and close document
            uploaded_file.seek(0)
            pdf_document.close()
        except Exception as e:
            st.error(f"Error previewing PDF: {e}")
    # st.markdown('</div>', unsafe_allow_html=True)

# Analysis Options
st.markdown('<div class="sub-header">Choose Analysis Type</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("📋 Resume Review")
    submit3 = st.button("📊 Match Percentage")

with col2:
    submit2 = st.button("📈 Skills Improvement")
    submit4 = st.button("🔍 ATS Score Check")

# Divider
st.markdown("---")

# Prompt templates
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

# Results section
if any([submit1, submit2, submit3, submit4]):
    if uploaded_file is None:
        st.error("⚠️ Please upload your resume first")
    elif not input_text.strip():
        st.error("⚠️ Please enter a job description")
    else:
        with st.spinner("Analyzing your resume..."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                if submit1:
                    analysis_type = "Resume Review"
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                elif submit2:
                    analysis_type = "Skills Improvement"
                    response = get_gemini_response(input_prompt2, pdf_content, input_text)
                elif submit3:
                    analysis_type = "Match Percentage"
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                elif submit4:
                    analysis_type = "ATS Score Check"
                    response = get_gemini_response(input_prompt4, pdf_content, input_text)
                
                # st.markdown(f'<div class="results-section">', unsafe_allow_html=False)
                st.markdown(f'<div class="sub-header">{analysis_type} Results</div>', unsafe_allow_html=True)
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save option
                if st.button("📥 Save Results", key="save_results"):
                    with st.spinner("Preparing download..."):
                        download_text = f"# {analysis_type} Results\n\n{response}"
                        st.download_button(
                            label="Download Results as Text",
                            data=download_text,
                            file_name=f"resume_{analysis_type.lower().replace(' ', '_')}.txt",
                            mime="text/plain",
                            key="download_button"
                        )
            except Exception as e:
                st.error(f"An error occurred: {e}")