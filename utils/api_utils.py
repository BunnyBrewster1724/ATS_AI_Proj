import os
import requests
import json
import google.generativeai as genai

def get_gemini_response(input_prompt, pdf_content, job_description):
    """
    Get response from Google Gemini API
    
    Args:
        input_prompt: The prompt for Gemini
        pdf_content: The processed PDF content
        job_description: The job description text
        
    Returns:
        Text response from Gemini
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(contents=[input_prompt, pdf_content[0], job_description])
    return response.text

def fetch_jobs_api(job_role, location, remote_only=False, page=1, api_key=None):
    """
    Fetch jobs from JSearch API
    
    Args:
        job_role: Job title to search for
        location: Location to search in
        remote_only: Whether to search for remote jobs only
        page: Page number for pagination
        api_key: RapidAPI key for JSearch
        
    Returns:
        List of job postings or empty list if error
    """
    if not api_key:
        api_key = os.getenv("JSEARCH_API_KEY", "e534334fbdmsh2a9700703dd7a6bp1ce194jsn0066e50a0a44")
    
    url = "https://jsearch.p.rapidapi.com/search"
    
    # Prepare query parameters
    query = f"{job_role} in {location}"
    if remote_only:
        query = f"remote {job_role} in {location}"
    
    querystring = {
        "query": query,
        "page": str(page),
        "num_pages": "1",
        "date_posted": "all",
        "remote_jobs_only": "true" if remote_only else "false",
        "employment_types": "FULLTIME,CONTRACTOR,PARTTIME,INTERN"
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        
        # Check for rate limiting or other errors
        if response.status_code == 429:
            return {"error": "API Rate limit exceeded. Please try again later."}
        
        # Check for any other non-200 responses
        if response.status_code != 200:
            return {"error": f"API Error: Status code {response.status_code}"}
        
        # Process successful response
        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            return {"error": "No jobs found or invalid response format."}
                
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Error: Invalid JSON response from API"}

def fetch_salary_estimate(job_title, location, experience="ALL", api_key=None):
    """
    Fetch salary estimate from JSearch API
    
    Args:
        job_title: Job title to get salary for
        location: Location to get salary for
        experience: Experience level
        api_key: RapidAPI key for JSearch
        
    Returns:
        Salary data or error message
    """
    if not api_key:
        api_key = os.getenv("JSEARCH_API_KEY", "e534334fbdmsh2a9700703dd7a6bp1ce194jsn0066e50a0a44")
    
    url = "https://jsearch.p.rapidapi.com/estimated-salary"
    
    querystring = {
        "job_title": job_title,
        "location": location,
        "radius": "100",
        "location_type": "ANY",
        "years_of_experience": experience
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        
        # Handle rate limiting
        if response.status_code == 429:
            return {"error": "API Rate limit exceeded. Please try again later."}
        
        # Handle other errors
        if response.status_code != 200:
            return {"error": f"API Error: Status code {response.status_code}"}
        
        # Process successful response
        data = response.json()
        if "data" in data and data["data"]:
            return data["data"][0]
        else:
            return {"error": "No salary data available for this job and location"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Error: Invalid JSON response from API"}