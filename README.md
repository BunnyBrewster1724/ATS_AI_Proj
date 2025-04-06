# ATS Resume Analyzer & Job Search

An all-in-one application to analyze your resume against job descriptions, match your skills to job listings, search for real-time job opportunities, and get salary estimates - all powered by AI.

## Features

- **Resume Analysis**: Get AI-powered feedback on how well your resume matches specific job descriptions
- **Job Matching**: Find job matches based on your skills from our database
- **Real-Time Job Search**: Search for the latest job postings matching your profile
- **Salary Estimates**: Get salary insights for your target role and location

## Project Structure

```
ats_resume_analyzer/
├── app.py                  # Main application entry point
├── requirements.txt        # All dependencies
├── .env                    # For API keys (create this file)
├── data/                   # For data files like cleaned_job_skills.csv
├── modules/
│   ├── resume_analyzer.py  # Resume analysis functions
│   ├── job_matcher.py      # Existing job matching from skills
│   ├── job_search.py       # New real-time job search functionality
│   └── ui_components.py    # Common UI elements and styles
└── utils/
    ├── pdf_utils.py        # PDF handling functions
    └── api_utils.py        # API interaction utilities
```

## Setup Instructions

1. Clone the repository or download the source code
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your API keys:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   JSEARCH_API_KEY=your_jsearch_api_key
   ```
5. Create a `data` directory and place your cleaned_job_skills.csv file in it

## API Keys

- **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/)
- **JSearch API Key**: Get from [RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

## Running the Application

```
streamlit run app.py
```

## Dependencies

- streamlit
- python-dotenv
- PyMuPDF
- pandas
- scikit-learn
- Pillow
- google-generativeai
- requests
- python-dateutil

## Features in Detail

### Resume Analysis
Upload your resume and paste a job description to get:
- Resume review
- Skills improvement suggestions
- Match percentage
- ATS score check

### Job Matching
Find jobs that match your skills:
- Upload your resume or enter skills manually
- Get matches from our job database
- See match percentage and required skills

### Real-Time Job Search
Search for jobs from live job boards:
- Search by title and location
- Filter for remote positions
- Get detailed job information
- Apply directly via job links

### Salary Estimates
Get salary insights:
- Search by job title and location
- Filter by experience level
- See minimum, median, and maximum salary ranges