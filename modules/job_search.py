import streamlit as st
import time
from datetime import datetime, timezone
from dateutil import parser
from utils.api_utils import fetch_jobs_api, fetch_salary_estimate
from utils.pdf_utils import extract_text_from_pdf
from modules.resume_analyzer import extract_skills_from_text

def format_posted_date(posted_date):
    """
    Format the job posted date to a human-readable format
    
    Args:
        posted_date: ISO date string
        
    Returns:
        Human-readable date string (e.g., "Today", "Yesterday", "3 days ago")
    """
    try:
        date_obj = parser.parse(posted_date)
        now = datetime.now(timezone.utc)
        
        # Calculate days ago
        days_ago = (now - date_obj).days
        if days_ago == 0:
            return "Today"
        elif days_ago == 1:
            return "Yesterday"
        else:
            return f"{days_ago} days ago"
    except:
        # If date parsing fails, keep the original
        return "Recently"

def extract_job_title_from_resume(resume_text):
    """
    Extract the most recent job title from resume text
    This is a simplified implementation that could be enhanced with ML
    
    Args:
        resume_text: Full text of the resume
        
    Returns:
        Estimated job title
    """
    # This is a very basic implementation - in a real app, you'd use a more sophisticated approach
    common_titles = [
        "Software Engineer", "Data Scientist", "Product Manager", "Data Analyst",
        "Web Developer", "Front End Developer", "Back End Developer", "Full Stack Developer",
        "UI/UX Designer", "Project Manager", "Business Analyst", "Marketing Manager"
    ]
    
    # Find which titles appear in the resume
    found_titles = [title for title in common_titles if title.lower() in resume_text.lower()]
    
    if found_titles:
        return found_titles[0]
    else:
        # Default fallback
        return "Software Engineer"

def render_job_search_tab():
    """Render the real-time job search tab in the Streamlit UI"""
    st.markdown('<div class="sub-header">Real-Time Job Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Find the latest job opportunities matching your profile</div>', unsafe_allow_html=True)
    
    # Column layout for search inputs
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("### Job Title")
        default_job_title = ""
        
        # Check if we have a resume from a previous tab
        if 'resume_text' in st.session_state:
            default_job_title = extract_job_title_from_resume(st.session_state.resume_text)
        
        job_role = st.text_input("Job Title", value=default_job_title, label_visibility="collapsed")
    
    with col2:
        st.markdown("### Location")
        job_location = st.text_input("Location", value="India", label_visibility="collapsed")
    
    with col3:
        st.markdown("&nbsp;")  # Empty header for alignment
        remote_only = st.checkbox("Remote Only", value=False)
    
    # Settings row
    col1, col2 = st.columns([1, 3])
    
    with col1:
        results_count = st.selectbox("Results to show:", options=[10, 20, 30, 50, 100], index=1)
    
    # Search button row
    col1, col2 = st.columns([1, 3])
    with col1:
        search_button = st.button("🔍 Search Jobs", use_container_width=True)
    
    # Option to upload resume if not already uploaded
    if 'resume_text' not in st.session_state:
        with st.expander("Upload Resume for Better Job Matching"):
            job_search_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="job_search_upload")
            
            if job_search_file is not None:
                resume_text = extract_text_from_pdf(job_search_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    job_title_suggestion = extract_job_title_from_resume(resume_text)
                    st.success(f"✅ Resume analyzed. Suggested job title: {job_title_suggestion}")
    
    # Check if we should automatically trigger a search (from another tab)
    if 'trigger_job_search' in st.session_state and st.session_state.trigger_job_search:
        search_button = True
        st.session_state.trigger_job_search = False  # Reset trigger

    # Results section
    if search_button:
        if not job_role.strip():
            st.error("⚠️ Please enter a job title")
        else:
            with st.spinner(f"Searching for {job_role} jobs in {job_location}..."):
                # Calculate pages needed (10 results per page from the API)
                pages_needed = (results_count + 9) // 10  # Ceiling division
                all_jobs = []
                
                progress_bar = st.progress(0)
                
                # Fetch multiple pages if needed
                for page in range(1, pages_needed + 1):
                    progress_text = st.empty()
                    progress_text.text(f"Fetching page {page} of {pages_needed}...")
                    
                    # Fetch jobs from JSearch API
                    new_jobs = fetch_jobs_api(job_role, job_location, remote_only, page)
                    
                    if isinstance(new_jobs, dict) and "error" in new_jobs:
                        st.error(new_jobs["error"])
                        break
                    
                    if not new_jobs:
                        # No more results
                        break
                    
                    all_jobs.extend(new_jobs)
                    progress_bar.progress(page / pages_needed)
                    
                    # Don't overwhelm the API
                    if page < pages_needed:
                        time.sleep(1)
                
                # Limit to requested number
                all_jobs = all_jobs[:results_count]
                progress_bar.progress(100)
                
                if all_jobs:
                    st.success(f"Found {len(all_jobs)} job listings")
                    
                    # Display results
                    for i, job in enumerate(all_jobs):
                        with st.container():
                            # Create a card-like container for each job
                            st.markdown("""
                            <style>
                            .job-card {
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                padding: 15px;
                                margin-bottom: 15px;
                                background-color: #f9f9f9;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"<div class='job-card'>", unsafe_allow_html=True)
                            
                            # Extract job details
                            title = job.get("job_title", "Unknown Position")
                            company = job.get("employer_name", "Unknown Company")
                            
                            # Handle location data safely
                            job_city = job.get("job_city", "")
                            job_state = job.get("job_state", "")
                            
                            # Handle None values for location fields
                            job_city = "" if job_city is None else job_city
                            job_state = "" if job_state is None else job_state
                                
                            location = ""
                            if job_city or job_state:
                                location = f"{job_city}, {job_state}".strip().rstrip(',').lstrip(',')
                            else:
                                location = job.get("job_country", "Remote")
                                
                            job_type = job.get("job_employment_type", "Full-time")
                            posted_date = job.get("job_posted_at_datetime_utc", "Recently")
                            job_url = job.get("job_apply_link", "")
                            
                            # Format date
                            posted_date_formatted = format_posted_date(posted_date)
                            
                            # Display job information
                            st.markdown(f"### {title}")
                            st.markdown(f"**{company}** • {location} • {job_type}")
                            st.markdown(f"Posted: {posted_date_formatted}")
                            
                            # Display salary if available
                            if job.get("job_min_salary") or job.get("job_max_salary"):
                                min_salary = job.get("job_min_salary", "")
                                max_salary = job.get("job_max_salary", "")
                                salary_currency = job.get("job_salary_currency", "$")
                                salary_period = job.get("job_salary_period", "YEAR")
                                
                                # Format salary period
                                if salary_period == "YEAR":
                                    period_text = "/year"
                                elif salary_period == "MONTH":
                                    period_text = "/month"
                                elif salary_period == "HOUR":
                                    period_text = "/hour"
                                else:
                                    period_text = ""
                                
                                # Display salary range
                                if min_salary and max_salary:
                                    salary_text = f"{salary_currency}{int(min_salary):,} - {salary_currency}{int(max_salary):,}{period_text}"
                                elif min_salary:
                                    salary_text = f"From {salary_currency}{int(min_salary):,}{period_text}"
                                elif max_salary:
                                    salary_text = f"Up to {salary_currency}{int(max_salary):,}{period_text}"
                                else:
                                    salary_text = ""
                                
                                if salary_text:
                                    st.markdown(f"**Salary:** {salary_text}")
                            
                            # Description (truncated)
                            description = job.get("job_description", "No description available.")
                            if len(description) > 500:
                                description = description[:500] + "..."
                            
                            with st.expander("Job Description"):
                                st.markdown(description)
                            
                            # Apply button
                            col1, col2 = st.columns([3, 1])
                            with col2:
                                st.markdown(f"[Apply Now]({job_url})")
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No job listings found. Try different search terms or location.")

def render_salary_tab():
    """Render the salary estimate tab in the Streamlit UI"""
    st.markdown('<div class="sub-header">Salary Estimates</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-text">Get salary insights for your target role and location</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Job Title")
        salary_job_title = st.text_input("Job Title", value="Enter desired job title", key="salary_job_title", label_visibility="collapsed")
    
    with col2:
        st.markdown("### Location")
        salary_location = st.text_input("Location", value="Enter country", key="salary_location", label_visibility="collapsed")
    
    # Experience dropdown
    experience_options = ["All Experience Levels", "Less than 1 year", "1-3 years", "4-6 years", "7-9 years", "10-14 years", "15+ years"]
    experience_values = ["ALL", "LESS_THAN_ONE", "ONE_TO_THREE", "FOUR_TO_SIX", "SEVEN_TO_NINE", "TEN_TO_FOURTEEN", "ABOVE_FIFTEEN"]
    experience_mapping = dict(zip(experience_options, experience_values))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Experience Level")
        selected_experience = st.selectbox("Experience", options=experience_options, index=0, label_visibility="collapsed")
    
    with col2:
        st.markdown("&nbsp;")  # Empty header for alignment
        get_salary_button = st.button("💰 Get Salary Estimate", use_container_width=True)
    
    # Handle salary estimate
    if get_salary_button:
        if not salary_job_title.strip() or not salary_location.strip():
            st.error("⚠️ Please enter both job title and location")
        else:
            with st.spinner("Fetching salary estimates..."):
                experience_code = experience_mapping.get(selected_experience, "ALL")
                salary_data = fetch_salary_estimate(salary_job_title, salary_location, experience_code)
                
                if isinstance(salary_data, dict) and "error" in salary_data:
                    st.error(salary_data["error"])
                else:
                    # Create a fancy salary display
                    st.markdown("""
                    <style>
                    .salary-card {
                        background-color: #f0f7ff;
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        margin: 20px 0;
                        border-left: 5px solid #1E88E5;
                    }
                    .salary-title {
                        font-size: 24px;
                        color: #0D47A1;
                        margin-bottom: 20px;
                    }
                    .salary-range {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 30px;
                    }
                    .salary-value {
                        text-align: center;
                        padding: 0 10px;
                    }
                    .salary-label {
                        font-size: 14px;
                        color: #555;
                        margin-bottom: 5px;
                    }
                    .min-value {
                        font-size: 20px;
                        color: #2E7D32;
                    }
                    .median-value {
                        font-size: 28px;
                        color: #1565C0;
                        font-weight: bold;
                    }
                    .max-value {
                        font-size: 20px;
                        color: #C62828;
                    }
                    .salary-source {
                        font-size: 12px;
                        color: #757575;
                        text-align: right;
                        margin-top: 10px;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Format salary values
                    min_salary = f"${int(salary_data.get('min_salary', 0)):,}" if 'min_salary' in salary_data else "--"
                    max_salary = f"${int(salary_data.get('max_salary', 0)):,}" if 'max_salary' in salary_data else "--"
                    median_salary = f"${int(salary_data.get('median_salary', 0)):,}" if 'median_salary' in salary_data else "--"
                    
                    st.markdown(f"""
                    <div class="salary-card">
                        <div class="salary-title">Salary Estimate for {salary_job_title} in {salary_location}</div>
                        <div class="salary-range">
                            <div class="salary-value">
                                <div class="salary-label">Minimum</div>
                                <div class="min-value">{min_salary}</div>
                            </div>
                            <div class="salary-value">
                                <div class="salary-label">Median</div>
                                <div class="median-value">{median_salary}</div>
                            </div>
                            <div class="salary-value">
                                <div class="salary-label">Maximum</div>
                                <div class="max-value">{max_salary}</div>
                            </div>
                        </div>
                        <div class="salary-source">Source: {salary_data.get('publisher_name', 'JSearch')} • Last updated: {salary_data.get('last_updated', 'Recently')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Additional info
                    with st.expander("Salary Insights"):
                        st.markdown("""
                        ### How to Use This Information
                        
                        - **Negotiating Offers:** Use the median and maximum figures as reference points when negotiating job offers.
                        - **Career Planning:** Understand how experience levels affect compensation in your field.
                        - **Regional Differences:** Be aware that salaries vary significantly by location, even for the same role.
                        
                        ### Factors Affecting Salary
                        
                        - Experience level
                        - Company size and industry
                        - Specific technical skills
                        - Education and certifications
                        - Location and cost of living
                        """)