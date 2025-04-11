import streamlit as st
import base64
from utils.pdf_utils import input_pdf_setup
from utils.api_utils import get_gemini_response

# Define prompt templates
PROMPT_TEMPLATES = {
    "resume_review": """
     You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
     Please share your professional evaluation on whether the candidate's profile aligns with the role. 
     Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """,
    
    "skills_improvement": """
     You are a Technical human resource manager with expertise in data science,
     your role is to scrutinize the resume in light of the job description provided. 
     Share your insights on the candidate's suitability for the role from an HR perspective. 
     Additionally, offer advice on enhancing the candidate's skills and identify areas with improvement.
    """,
    
    "match_percentage": """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, web development, big data engineering,
    data analyst and deep ATS functionality, 
    your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
    """,
    
    "ats_score": """
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
    """,
    
    "extract_skills": """
    Extract only the technical and professional skills from this resume text. 
    Format the output as a comma-separated list of skills ONLY, without explanations or headers.
    Example output: Python, SQL, Data Analysis, Project Management
    """
}

def analyze_resume(analysis_type, pdf_content, job_description):
    """
    Analyze resume based on the selected analysis type
    
    Args:
        analysis_type: Type of analysis to perform
        pdf_content: Processed PDF content
        job_description: Job description text
        
    Returns:
        Analysis results from Gemini
    """
    prompt = PROMPT_TEMPLATES.get(analysis_type)
    if not prompt:
        return "Invalid analysis type"
    
    return get_gemini_response(prompt, pdf_content, job_description)

def extract_skills_from_text(resume_text):
    """
    Extract skills from resume text using Gemini
    
    Args:
        resume_text: Plain text extracted from resume
        
    Returns:
        Comma-separated list of skills
    """
    prompt = PROMPT_TEMPLATES["extract_skills"]
    pdf_content = [
        {
            "mime_type": "text/plain",
            "data": base64.b64encode(resume_text.encode()).decode()
        }
    ]
    
    return get_gemini_response(prompt, pdf_content, "")

def render_resume_analysis_tab():
    """Render the resume analysis tab in the Streamlit UI"""
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
                from utils.pdf_utils import generate_pdf_preview
                img = generate_pdf_preview(uploaded_file)
                st.image(img, width=250, caption="Resume Preview")
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

    # Add button for real-time job search
    jobs_button = st.button("🔎 Find Matching Jobs")

    # Divider
    st.markdown("---")

    # Map buttons to analysis types
    button_to_analysis = {
        submit1: ("resume_review", "Resume Review"),
        submit2: ("skills_improvement", "Skills Improvement"),
        submit3: ("match_percentage", "Match Percentage"),
        submit4: ("ats_score", "ATS Score Check")
    }

    # Results section for analysis
    for button, (analysis_code, analysis_name) in button_to_analysis.items():
        if button:
            if uploaded_file is None:
                st.error("⚠️ Please upload your resume first")
            elif not input_text.strip():
                st.error("⚠️ Please enter a job description")
            else:
                with st.spinner("Analyzing your resume..."):
                    try:
                        pdf_content = input_pdf_setup(uploaded_file)
                        response = analyze_resume(analysis_code, pdf_content, input_text)
                        
                        st.markdown(f'<div class="sub-header">{analysis_name} Results</div>', unsafe_allow_html=True)
                        st.markdown(response)
                        
                        # Save option
                        if st.button("📥 Save Results", key="save_results"):
                            with st.spinner("Preparing download..."):
                                download_text = f"# {analysis_name} Results\n\n{response}"
                                st.download_button(
                                    label="Download Results as Text",
                                    data=download_text,
                                    file_name=f"resume_{analysis_code}.txt",
                                    mime="text/plain",
                                    key="download_button"
                                )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
    
    # Handle jobs button - Extract job title from resume for searching
    if jobs_button:
        if uploaded_file is None:
            st.error("⚠️ Please upload your resume first")
        else:
            # Store in session state to access in the job search tab
            if 'trigger_job_search' not in st.session_state:
                st.session_state.trigger_job_search = True
            
            # Extract skills for job search
            from utils.pdf_utils import extract_text_from_pdf
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text
            
            # Switch to job search tab programmatically
            # Note: Streamlit doesn't support direct tab switching, so we use instructions
            st.info("✨ Click on the 'Job Search' tab to see matching jobs based on your resume!")