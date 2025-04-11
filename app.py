import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Import modules
from modules.resume_analyzer import render_resume_analysis_tab
from modules.job_matcher import render_job_matching_tab
from modules.job_search import render_job_search_tab, render_salary_tab
from modules.ui_components import load_css, render_header, render_footer

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="ATS Resume Analyzer & Job Search", 
    page_icon="📝", 
    layout="wide"
)

# Load custom CSS
load_css()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GOOGLE_API_KEY not found in environment variables. Please add it to .env file.")

# Render application header
render_header()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Resume Analysis", 
    "🔍 Job Matching", 
    "🌐 Real-Time Jobs",
    "💰 Salary Estimates"
])

# Render content for each tab
with tab1:
    render_resume_analysis_tab()

with tab2:
    render_job_matching_tab()

with tab3:
    render_job_search_tab()

with tab4:
    render_salary_tab()

# Render footer
render_footer()