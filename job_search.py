import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import webbrowser
import threading
from datetime import datetime

class JobSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-time Job Search")
        self.root.geometry("900x700")
        
        # Job role synonyms dictionary
        self.job_synonyms = {
            "software engineer": ["software developer", "programmer", "coder", "application developer", 
                                 "software engineer", "full stack developer", "backend developer", 
                                 "frontend developer", "web developer"],
            "data scientist": ["data analyst", "machine learning engineer", "ai engineer", 
                              "data engineer", "data scientist", "ml engineer"],
            "product manager": ["product owner", "program manager", "project manager", 
                               "product management", "product lead"]
        }
        
        # Create UI elements
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Job role input
        ttk.Label(frame, text="Enter Job Role:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.job_role = ttk.Entry(frame, width=40)
        self.job_role.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)
        self.job_role.insert(0, "Software Engineer")
        
        # Location input
        ttk.Label(frame, text="Location:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.location = ttk.Entry(frame, width=40)
        self.location.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        self.location.insert(0, "United States")
        
        # API Key input (for security, in a real app, store this securely)
        ttk.Label(frame, text="API Key:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.api_key = ttk.Entry(frame, width=40, show="*")
        self.api_key.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        
        # Search button
        self.search_button = ttk.Button(frame, text="Search Jobs", command=self.start_search)
        self.search_button.grid(column=2, row=0, rowspan=3, padx=10)
        
        # Results area with hyperlinks
        ttk.Label(frame, text="Job Listings:").grid(column=0, row=3, sticky=tk.W, pady=5)
        
        # Frame for results with scrollbar
        results_frame = ttk.Frame(frame)
        results_frame.grid(column=0, row=4, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_canvas = tk.Canvas(results_frame)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.result_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.result_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.result_canvas.configure(
                scrollregion=self.result_canvas.bbox("all")
            )
        )
        
        self.result_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.result_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.result_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure grid expansion
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)
    
    def start_search(self):
        """Start search in a separate thread to keep UI responsive"""
        self.search_button.config(state="disabled")
        self.status_var.set("Searching...")
        
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        search_thread = threading.Thread(target=self.search_jobs)
        search_thread.daemon = True
        search_thread.start()
    
    def search_jobs(self):
        """Search for jobs based on input role"""
        try:
            job_role = self.job_role.get().strip()
            location = self.location.get().strip()
            api_key = self.api_key.get().strip()
            
            if not api_key:
                self.root.after(0, lambda: self.status_var.set("Error: API Key is required"))
                self.root.after(0, lambda: self.search_button.config(state="normal"))
                return
            
            # Get all possible search terms (the role itself + synonyms)
            search_terms = [job_role]
            
            # Add synonyms if available
            for key, synonyms in self.job_synonyms.items():
                if job_role.lower() in key or any(term in job_role.lower() for term in synonyms):
                    search_terms.extend(synonyms)
                    break
            
            # Remove duplicates
            search_terms = list(set(search_terms))
            
            all_jobs = []
            
            # Use the main search term for the API call
            jobs = self.fetch_jobs_api(search_terms[0], location, api_key)
            all_jobs.extend(jobs)
            
            # Display results
            self.display_results(all_jobs)
            
            self.status_var.set(f"Found {len(all_jobs)} job listings")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.search_button.config(state="normal"))
    
    def fetch_jobs_api(self, job_role, location, api_key):
        """Fetch jobs from API (Indeed via RapidAPI)"""
        url = "https://indeed-jobs-api.p.rapidapi.com/indeed-us"
        
        querystring = {
            "search_term": job_role,
            "location": location,
            "page": "1",
            "sort_by": "relevance"
        }
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "indeed-jobs-api.p.rapidapi.com"
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise exception for non-200 status codes
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "jobs" in data:
                    return data["jobs"]
                elif isinstance(data, list):
                    return data
                else:
                    return []
            else:
                return []
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"API Error: {str(e)}")
            return []
    
    def open_job_link(self, url):
        """Open job URL in default browser"""
        webbrowser.open_new(url)
    
    def display_results(self, jobs):
        """Display job results with clickable links"""
        if not jobs:
            no_jobs_label = ttk.Label(self.scrollable_frame, text="No job listings found. Try a different search term.")
            no_jobs_label.pack(pady=10, padx=10, anchor="w")
            return
        
        for i, job in enumerate(jobs, 1):
            # Create frame for job listing
            job_frame = ttk.Frame(self.scrollable_frame, relief="ridge", borderwidth=2)
            job_frame.pack(fill="x", padx=5, pady=5, expand=True)
            
            # Job title as hyperlink
            title = job.get("job_title", "Unknown Position")
            company = job.get("company_name", "Unknown Company")
            location = job.get("location", "Remote")
            posted_date = job.get("posted_date", "Recently")
            job_url = job.get("job_url", "")
            
            # Title with hyperlink
            title_link = ttk.Label(job_frame, text=title, foreground="blue", cursor="hand2", font=("", 12, "bold"))
            title_link.pack(anchor="w", padx=10, pady=(10, 5))
            title_link.bind("<Button-1>", lambda e, url=job_url: self.open_job_link(url))
            
            # Company and location
            ttk.Label(job_frame, text=f"{company} • {location}").pack(anchor="w", padx=10, pady=2)
            
            # Posted date
            ttk.Label(job_frame, text=f"Posted: {posted_date}").pack(anchor="w", padx=10, pady=2)
            
            # Description (truncated)
            description = job.get("job_description", "No description available.")
            if len(description) > 200:
                description = description[:200] + "..."
            
            description_text = ttk.Label(job_frame, text=description, wraplength=800)
            description_text.pack(anchor="w", padx=10, pady=(5, 10))
            
            # Apply button
            apply_button = ttk.Button(
                job_frame, 
                text="View Job", 
                command=lambda url=job_url: self.open_job_link(url)
            )
            apply_button.pack(anchor="e", padx=10, pady=(0, 10))

# For testing purposes when API key is not available
def fetch_mock_jobs():
    """Generate mock job listings for testing"""
    import random
    
    jobs = []
    companies = ["Tech Solutions Inc.", "Digital Innovations", "Code Masters", 
                "ByteCraft Technologies", "DevHub", "InnovateTech", "DataPulse"]
    
    locations = ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", 
                "Boston, MA", "Chicago, IL", "Remote"]
    
    descriptions = [
        "We are seeking a skilled software engineer to join our team. The ideal candidate will have experience with modern web technologies and a passion for creating clean, efficient code.",
        "Join our dynamic team building cutting-edge applications. You'll work in an agile environment with opportunities to grow and develop your skills.",
        "Looking for an experienced developer with skills in Python, JavaScript, and cloud technologies. You'll be working on scalable solutions for enterprise clients."
    ]
    
    for i in range(10):
        today = datetime.now()
        days_ago = random.randint(1, 30)
        
        job = {
            "job_title": f"Software Engineer {random.choice(['', 'I', 'II', 'III', 'Senior', 'Lead'])}",
            "company_name": random.choice(companies),
            "location": random.choice(locations),
            "posted_date": f"{days_ago} days ago",
            "job_description": random.choice(descriptions),
            "job_url": f"https://example.com/job/{i}",
            "salary": f"${random.randint(80, 150)}k - ${random.randint(150, 200)}k"
        }
        jobs.append(job)
    
    return jobs

if __name__ == "__main__":
    root = tk.Tk()
    app = JobSearchApp(root)
    root.mainloop()