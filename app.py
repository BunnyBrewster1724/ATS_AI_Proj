import base64
import io
from dotenv import load_dotenv
import fitz  # PyMuPDF
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📝", layout="wide")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
  
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    
    response = model.generate_content(contents=[input, pdf_content[0], prompt])
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
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

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        
        pdf_document.close()
        uploaded_file.seek(0)  # Reset file pointer
        return text
    else:
        return ""

def find_job_matches(user_skills, top_n=5):
    try:
        df = pd.read_csv("cleaned_job_skills copy.csv")
        df_cleaned = df.dropna(subset=['job_skills'])
        vectorizer = TfidfVectorizer()
        job_skill_vectors = vectorizer.fit_transform(df_cleaned['job_skills'])
        user_vector = vectorizer.transform([user_skills])
        similarities = cosine_similarity(user_vector, job_skill_vectors).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        top_jobs = df_cleaned.iloc[top_indices][['job_link', 'job_skills']]
        top_jobs['similarity_score'] = similarities[top_indices]
        top_jobs['similarity_percentage'] = (similarities[top_indices] * 100).round(2)
    
        return top_jobs
    except Exception as e:
        st.error(f"Error finding job matches: {e}")
        return pd.DataFrame()

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
    .job-match {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-header">ATS Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="info-text">Optimize your resume for Applicant Tracking Systems with AI-powered analysis</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Resume Analysis", "Job Matching"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Job Description")
        st.markdown("Paste the job description you're applying for:", unsafe_allow_html=True)
        input_text = st.text_area("Job Description", height=200, key="input", label_visibility="collapsed")

    with col2:
        st.markdown("### Upload Resume")
        uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="resume_upload", label_visibility="collapsed")
        
        if uploaded_file is not None:
            st.success("✅ Resume uploaded successfully!")
            try:
                pdf_bytes = uploaded_file.read()
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                first_page = pdf_document.load_page(0)
                pix = first_page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                st.image(img, width=250, caption="Resume Preview")
                uploaded_file.seek(0)
                pdf_document.close()
            except Exception as e:
                st.error(f"Error previewing PDF: {e}")

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
                    
                    st.markdown(f'<div class="sub-header">{analysis_type} Results</div>', unsafe_allow_html=True)
                    st.markdown(response)
                    
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

with tab2:
    st.markdown('<div class="sub-header">Job Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Find job matches based on your skills from our database</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Resume for Skills")
        job_match_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="job_match_upload", label_visibility="collapsed")
        
        if job_match_file is not None:
            st.success("✅ Resume uploaded for job matching")
            resume_text = extract_text_from_pdf(job_match_file)
            if resume_text:
                with st.spinner("Extracting skills from resume..."):
                    skill_prompt = """
                    Extract only the technical and professional skills from this resume text. 
                    Format the output as a comma-separated list of skills ONLY, without explanations or headers.
                    Example output: Python, SQL, Data Analysis, Project Management
                    """
                    pdf_content = [
                        {
                            "mime_type": "text/plain",
                            "data": base64.b64encode(resume_text.encode()).decode()
                        }
                    ]
                    
                    extracted_skills = get_gemini_response("", pdf_content, skill_prompt)
    
    with col2:
        st.markdown("### Or Enter Your Skills Manually")
        manual_skills = st.text_area(
            "Enter your skills (comma-separated)",
            placeholder="e.g. Python, SQL, Machine Learning, Project Management",
            height=100,
            key="manual_skills",
            label_visibility="collapsed"
        )

    if job_match_file is not None and 'extracted_skills' in locals():
        user_skills = extracted_skills
        st.info(f"Extracted skills: {extracted_skills}")
    else:
        user_skills = manual_skills
    if st.button("🔍 Find Matching Jobs", key="find_jobs"):
        if not user_skills:
            st.error("Please enter skills or upload a resume first")
        else:
            with st.spinner("Finding job matches..."):
                #num_matches = st.slider("Number of matches to show", 3, 10, 5)
                matches = find_job_matches(user_skills)
                
                if not matches.empty:
                    st.markdown('<div class="sub-header">Top Job Matches</div>', unsafe_allow_html=True)
                    
                    for idx, row in matches.iterrows():
                        st.markdown(f"""
                        <div class="job-match">
                            <h4>Match #{idx+1} - {row['similarity_percentage']}% Match</h4>
                            <p><strong>Job Link:</strong> <a href="{row['job_link']}" target="_blank">{row['job_link']}</a></p>
                            <p><strong>Required Skills:</strong> {row['job_skills']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No matching jobs found. Try adjusting your skills or adding more relevant ones.")