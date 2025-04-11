import streamlit as st

def load_css():
    """Load custom CSS for the application"""
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
        /* New styles for job cards */
        .job-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
            transition: transform 0.2s;
        }
        .job-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1E88E5;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header"""
    st.markdown('<div class="main-header">ATS Resume Analyzer & Job Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Optimize your resume for Applicant Tracking Systems and find matching jobs with AI-powered analysis</div>', unsafe_allow_html=True)

def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        ATS Resume Analyzer & Job Search - Your career success companion
    </div>
    """, unsafe_allow_html=True)