import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.pdf_utils import extract_text_from_pdf
from modules.resume_analyzer import extract_skills_from_text

def find_job_matches(user_skills, top_n=5):
    """
    Find job matches based on user skills using TF-IDF and cosine similarity
    
    Args:
        user_skills: Comma-separated string of user skills
        top_n: Number of top matches to return
        
    Returns:
        DataFrame with top matching jobs
    """
    try: 
        #df = pd.read_csv("/Users/chinku/git/ATS_AI_Proj/cleaned_job_skills.csv")
        df = pd.read_csv("data/cleaned_job_skills.csv")

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

def render_job_matching_tab():
    """Render the job matching tab in the Streamlit UI"""
    st.markdown('<div class="sub-header">Job Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Find job matches based on your skills from our database</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Resume for Skills")
        job_match_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="job_match_upload", label_visibility="collapsed")
        
        # Check if we came from the analysis tab with a resume
        if 'resume_text' in st.session_state and job_match_file is None:
            st.info("Using the resume you already uploaded.")
            extracted_skills = extract_skills_from_text(st.session_state.resume_text)
            st.success("✅ Skills extracted from your resume")
        elif job_match_file is not None:
            st.success("✅ Resume uploaded for job matching")
            resume_text = extract_text_from_pdf(job_match_file)
            if resume_text:
                with st.spinner("Extracting skills from resume..."):
                    extracted_skills = extract_skills_from_text(resume_text)
    
    with col2:
        st.markdown("### Or Enter Your Skills Manually")
        manual_skills = st.text_area(
            "Enter your skills (comma-separated)",
            placeholder="e.g. Python, SQL, Machine Learning, Project Management",
            height=100,
            key="manual_skills",
            label_visibility="collapsed"
        )

    # Determine which skills to use
    if 'resume_text' in st.session_state and job_match_file is None and 'extracted_skills' in locals():
        user_skills = extracted_skills
        st.info(f"Extracted skills: {extracted_skills}")
    elif job_match_file is not None and 'extracted_skills' in locals():
        user_skills = extracted_skills
        st.info(f"Extracted skills: {extracted_skills}")
    else:
        user_skills = manual_skills
        
    if st.button("🔍 Find Matching Jobs", key="find_jobs"):
        if not user_skills:
            st.error("Please enter skills or upload a resume first")
        else:
            with st.spinner("Finding job matches..."):
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
                    
    # Clear session if user interacts with this tab directly
    if job_match_file is not None and 'resume_text' in st.session_state:
        del st.session_state.resume_text
        if 'trigger_job_search' in st.session_state:
            del st.session_state.trigger_job_search