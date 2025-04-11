import streamlit as st

def load_css():
    """Load custom CSS for the application with beige/brown tones"""
    st.markdown("""
    <style>
    /* Color palette */
    :root {
        --primary-dark: #8B7355;      /* Dark brown */
        --primary: #A68064;           /* Medium brown */
        --primary-light: #D2B48C;     /* Tan */
        --secondary-light: #F5F5DC;   /* Beige */
        --accent: #CD853F;            /* Peru/Copper */
        --text-dark: #5D4037;         /* Dark brown text */
        --text-medium: #6D4C41;       /* Medium brown text */
        --text-light: #8D6E63;        /* Light brown text */
        --background: #EDE8D0;        /* Cream background */
        --background-light: #F2B949;  /* Mimosa */
        --success: #8D8741;           /* Olive green for success */
    }
    
    /* Main container & background */
    .main .block-container {
        padding: 2rem;
        background-color: var(--background);
    }
    
    /* Headers */
    .main-header {
        font-size: 2.8rem;
        color: #8B7355;
        font-weight: bold;
        margin-bottom: 0.2rem;
        font-family: 'Georgia', serif;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        font-spacing: 0.1rem;
    }
    .sub-header-text { 
        font-size: 1.2rem;
        color: #A68064;
        margin-bottom: 1rem;
        font-style: italic;
        text-align: center;
    }
    
    /* Text elements */
    .info-text {
        font-size: 1rem;
        color: var(--text-medium);
        line-height: 1.6;
        text-align: center;
    }
    
    /* Highlight sections */
    .highlight {
        background-color: var(--secondary-light);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 3px solid var(--primary);
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Upload section */
    .upload-section {
        border: 2px dashed var(--primary-light);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: var(--background-light);
        text-align: center;
    }
    
    /* Results section */
    .results-section {
        background-color: var(--secondary-light);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
        border-left: 5px solid var(--primary);
    }
    
    /* Job match element */
    .job-match {
        background-color: #f0ebe1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--success);
    }
    
    /* Job cards */
    .job-card {
        border: 1px solid #e0d6c6;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #faf7f0;
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 10px rgba(139, 115, 85, 0.2);
    }
    
    /* Card title & content */
    .card-title {
        font-weight: bold;
        color: var(--primary-dark);
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .card-subtitle {
        color: var(--text-light);
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: var(--background-light);
        padding: 10px 10px 10px 10px;
        border-radius: 8px 8px 0 0;
        align-items: center;
        display: flex;
        justify-content: center;
        border: 1px solid var(--primary-light);
        border-bottom: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0ebe1;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        font-weight: 500;
        color: var(--text-medium);
        border: none;
        align-items: center;
        display: flex;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: var(--primary);
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] div {
        background-color: var(--primary-light);
    }
    
    .stSlider [data-baseweb="thumb"] {
        background-color: var(--primary);
    }
    
    /* Text inputs */
    .stTextInput>div>div>input {
        border-radius: 4px;
        border: 1px solid #e0d6c6;
    }
    
    .stTextInput>div>div>input:focus {
        border: 2px solid var(--primary);
        box-shadow: 0 0 0 1px var(--primary-light);
    }
    
    /* Selectbox */
    .stSelectbox>div>div>div {
        background-color: white;
        border: 1px solid #e0d6c6;
    }
    
    /* Alert/Info boxes */
    .stAlert {
        background-color: #f0ebe1;
        border-left-color: var(--primary);
    }
    .resu-text {
    color: #8B7355;
    }
    .match-text {
    color: #CD853F;
    font-style: italic;
    
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header"""
    st.markdown('<div class="main-header"><span class="resu-text">Resu</span><span class="match-text">Match</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header-text">Resume Analysis & Job Search Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Optimize your resume for Applicant Tracking Systems and find matching jobs with AI-powered analysis</div>', unsafe_allow_html=True)

def render_footer():
    """Render the application footer with updated styling"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8D6E63; font-size: 0.8rem; padding: 1rem 0;">
        ATS Resume Analyzer & Job Search - Your career success companion
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load the custom CSS
    load_css()
    
    # Render the header
    render_header()
    
    # App tabs
    tabs = st.tabs(["Resume Analysis", "Job Search", "Career Tips"])
    
    with tabs[0]:
        st.markdown('<div class="sub-header">Resume Analysis</div>', unsafe_allow_html=True)
        
        # Upload section with improved styling
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        st.markdown('<p class="info-text">Or paste job description below to analyze compatibility</p>', unsafe_allow_html=True)
        st.text_area("Job Description", height=150)
        st.button("Analyze Resume")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Results section (initially hidden, would show after analysis)
        # Placeholder for demonstration
        with st.expander("View Sample Results"):
            st.markdown('<div class="results-section">', unsafe_allow_html=True)
            st.markdown('<div class="sub-header" style="font-size: 1.5rem;">Analysis Results</div>', unsafe_allow_html=True)
            st.progress(75)
            st.markdown("<p>Your resume is <b>75% compatible</b> with the job description</p>", unsafe_allow_html=True)
            
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.markdown("<h4>Key Findings</h4>", unsafe_allow_html=True)
            st.markdown("✅ Strong technical skills match")
            st.markdown("❌ Missing keywords: 'project management', 'agile methodology'")
            st.markdown("⚠️ Education section could be improved")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="sub-header">Find Matching Jobs</div>', unsafe_allow_html=True)
        st.text_input("Job Title")
        st.text_input("Location")
        st.slider("Experience (Years)", 0, 15, 3)
        st.button("Search Jobs")
        
        # Sample job results
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Senior Software Engineer</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">TechCorp Inc. • San Francisco, CA • Remote</div>', unsafe_allow_html=True)
        st.markdown("Looking for experienced developer with 3+ years in Python and cloud technologies.")
        st.markdown('<div style="display: flex; justify-content: space-between; margin-top: 10px;">', unsafe_allow_html=True)
        st.markdown('<span style="color: #8D8741; font-weight: bold;">Match: 92%</span>', unsafe_allow_html=True)
        st.markdown('<span style="color: #6D4C41;">$120K - $150K</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Full Stack Developer</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Innovative Solutions • Chicago, IL • Hybrid</div>', unsafe_allow_html=True)
        st.markdown("Join our team building next-gen web applications with React and Django.")
        st.markdown('<div style="display: flex; justify-content: space-between; margin-top: 10px;">', unsafe_allow_html=True)
        st.markdown('<span style="color: #8D8741; font-weight: bold;">Match: 87%</span>', unsafe_allow_html=True)
        st.markdown('<span style="color: #6D4C41;">$100K - $130K</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="sub-header">Career Tips</div>', unsafe_allow_html=True)
        st.markdown('<div class="highlight">', unsafe_allow_html=True)
        st.markdown("<h4>Resume Optimization Tips</h4>", unsafe_allow_html=True)
        st.markdown("1. Tailor your resume for each job application")
        st.markdown("2. Use industry-specific keywords from the job description")
        st.markdown("3. Quantify your achievements with numbers and metrics")
        st.markdown("4. Keep formatting clean and ATS-friendly")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="highlight">', unsafe_allow_html=True)
        st.markdown("<h4>Interview Preparation</h4>", unsafe_allow_html=True)
        st.markdown("1. Research the company thoroughly")
        st.markdown("2. Prepare STAR method responses for behavioral questions")
        st.markdown("3. Practice technical skills relevant to the position")
        st.markdown("4. Prepare thoughtful questions to ask your interviewer")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Render the footer
    render_footer()

if __name__ == "__main__":
    main()