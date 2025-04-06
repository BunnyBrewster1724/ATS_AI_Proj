import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import webbrowser
import threading
from datetime import datetime
import time
import traceback
from urllib.parse import quote

class JobSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSearch Job Search Application")
        self.root.geometry("900x700")
        
        # Create UI elements
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Job Search
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Job Search")
        
        # Tab 2: Salary Estimate
        salary_frame = ttk.Frame(notebook)
        notebook.add(salary_frame, text="Salary Estimate")
        
        # Set up Job Search tab
        self.setup_job_search_tab(search_frame)
        
        # Set up Salary Estimate tab
        self.setup_salary_tab(salary_frame)
        
        # Status bar for the entire app
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Default API key (you provided)
        self.default_api_key = "e534334fbdmsh2a9700703dd7a6bp1ce194jsn0066e50a0a44"
        
        # Initialize job count label
        self.job_count_var = tk.StringVar(value="")
    
    def setup_job_search_tab(self, parent_frame):
        """Set up the job search tab UI elements"""
        # Job role input
        ttk.Label(parent_frame, text="Job Title:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.job_role = ttk.Entry(parent_frame, width=40)
        self.job_role.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)
        self.job_role.insert(0, "Software Engineer")
        
        # Location input
        ttk.Label(parent_frame, text="Location:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.job_location = ttk.Entry(parent_frame, width=40)
        self.job_location.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        self.job_location.insert(0, "India")
        
        # Remote jobs only checkbox
        self.remote_var = tk.BooleanVar()
        remote_check = ttk.Checkbutton(parent_frame, text="Remote Jobs Only", variable=self.remote_var)
        remote_check.grid(column=1, row=2, sticky=tk.W, pady=5)
        
        # Number of results to show
        ttk.Label(parent_frame, text="Results to show:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.results_var = tk.StringVar(value="20")
        results_combobox = ttk.Combobox(parent_frame, textvariable=self.results_var, values=["10", "20", "30", "50", "100"], width=5)
        results_combobox.grid(column=1, row=3, sticky=tk.W, pady=5)
        
        # Search button
        self.search_button = ttk.Button(parent_frame, text="Search Jobs", command=self.start_job_search)
        self.search_button.grid(column=2, row=0, rowspan=2, padx=10)
        
        # Job count display
        self.job_count_var = tk.StringVar(value="")
        self.job_count_label = ttk.Label(parent_frame, textvariable=self.job_count_var, anchor="w")
        self.job_count_label.grid(column=0, row=4, columnspan=3, sticky=tk.W, pady=5)
        
        # Results area
        ttk.Label(parent_frame, text="Job Listings:").grid(column=0, row=5, sticky=tk.W, pady=5)
        
        # Frame for results with scrollbar
        results_frame = ttk.Frame(parent_frame)
        results_frame.grid(column=0, row=6, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.job_result_canvas = tk.Canvas(results_frame)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.job_result_canvas.yview)
        self.job_scrollable_frame = ttk.Frame(self.job_result_canvas)
        
        self.job_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.job_result_canvas.configure(
                scrollregion=self.job_result_canvas.bbox("all")
            )
        )
        
        self.job_result_canvas.create_window((0, 0), window=self.job_scrollable_frame, anchor="nw")
        self.job_result_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.job_result_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid expansion
        parent_frame.columnconfigure(1, weight=1)
        parent_frame.rowconfigure(6, weight=1)
    
    def setup_salary_tab(self, parent_frame):
        """Set up the salary estimate tab UI elements"""
        # Job title input
        ttk.Label(parent_frame, text="Job Title:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.salary_job_title = ttk.Entry(parent_frame, width=40)
        self.salary_job_title.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)
        self.salary_job_title.insert(0, "Data Scientist")
        
        # Location input
        ttk.Label(parent_frame, text="Location:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.salary_location = ttk.Entry(parent_frame, width=40)
        self.salary_location.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        self.salary_location.insert(0, "India")
        
        # Experience dropdown - FIXED with correct API values
        ttk.Label(parent_frame, text="Experience:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.experience_var = tk.StringVar()
        experience_options = ["All Experience Levels", "Less than 1 year", "1-3 years", "4-6 years", "7-9 years", "10-14 years", "15+ years"]
        experience_values = ["ALL", "LESS_THAN_ONE", "ONE_TO_THREE", "FOUR_TO_SIX", "SEVEN_TO_NINE", "TEN_TO_FOURTEEN", "ABOVE_FIFTEEN"]
        self.experience_mapping = dict(zip(experience_options, experience_values))
        
        experience_dropdown = ttk.Combobox(parent_frame, textvariable=self.experience_var, values=experience_options)
        experience_dropdown.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        experience_dropdown.current(0)
        
        # Get Salary button
        self.salary_button = ttk.Button(parent_frame, text="Get Salary Estimate", command=self.start_salary_search)
        self.salary_button.grid(column=2, row=0, rowspan=2, padx=10)
        
        # Error message display
        self.error_var = tk.StringVar(value="")
        self.error_label = ttk.Label(parent_frame, textvariable=self.error_var, foreground="red", wraplength=800)
        self.error_label.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Results area
        self.salary_result_frame = ttk.LabelFrame(parent_frame, text="Salary Estimates")
        self.salary_result_frame.grid(column=0, row=4, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Initial empty labels
        self.min_salary_var = tk.StringVar(value="--")
        self.max_salary_var = tk.StringVar(value="--")
        self.median_salary_var = tk.StringVar(value="--")
        
        # Salary display
        salary_display_frame = ttk.Frame(self.salary_result_frame)
        salary_display_frame.pack(fill="x", expand=True, padx=20, pady=10)
        
        # Min salary
        min_frame = ttk.Frame(salary_display_frame)
        min_frame.pack(side="left", expand=True, fill="x")
        ttk.Label(min_frame, text="Minimum", font=("", 10, "bold")).pack(anchor="center")
        ttk.Label(min_frame, textvariable=self.min_salary_var, font=("", 16)).pack(anchor="center")
        
        # Median salary
        median_frame = ttk.Frame(salary_display_frame)
        median_frame.pack(side="left", expand=True, fill="x")
        ttk.Label(median_frame, text="Median", font=("", 10, "bold")).pack(anchor="center")
        ttk.Label(median_frame, textvariable=self.median_salary_var, font=("", 20, "bold")).pack(anchor="center")
        
        # Max salary
        max_frame = ttk.Frame(salary_display_frame)
        max_frame.pack(side="left", expand=True, fill="x")
        ttk.Label(max_frame, text="Maximum", font=("", 10, "bold")).pack(anchor="center")
        ttk.Label(max_frame, textvariable=self.max_salary_var, font=("", 16)).pack(anchor="center")
        
        # Source info
        self.salary_source_var = tk.StringVar(value="")
        ttk.Label(self.salary_result_frame, textvariable=self.salary_source_var, font=("", 8)).pack(side="bottom", anchor="e", padx=5)
        
        # Configure grid expansion
        parent_frame.columnconfigure(1, weight=1)
        parent_frame.rowconfigure(4, weight=1)
    
    def start_job_search(self):
        """Start job search in a separate thread to keep UI responsive"""
        self.search_button.config(state="disabled")
        self.status_var.set("Searching for jobs...")
        self.job_count_var.set("Searching...")
        
        # Clear previous results
        for widget in self.job_scrollable_frame.winfo_children():
            widget.destroy()
        
        search_thread = threading.Thread(target=self.search_jobs)
        search_thread.daemon = True
        search_thread.start()
    
    def start_salary_search(self):
        """Start salary search in a separate thread"""
        self.salary_button.config(state="disabled")
        self.status_var.set("Fetching salary estimates...")
        
        # Reset salary displays
        self.min_salary_var.set("--")
        self.max_salary_var.set("--")
        self.median_salary_var.set("--")
        self.salary_source_var.set("")
        self.error_var.set("")
        
        salary_thread = threading.Thread(target=self.fetch_salary_estimate)
        salary_thread.daemon = True
        salary_thread.start()
    
    def search_jobs(self):
        """Search for jobs based on input role"""
        try:
            job_role = self.job_role.get().strip()
            location = self.job_location.get().strip()
            remote_only = self.remote_var.get()
            num_results = int(self.results_var.get())
            
            # Calculate pages needed (10 results per page)
            pages_needed = (num_results + 9) // 10  # Ceiling division
            
            all_jobs = []
            
            # Fetch multiple pages if needed
            for page in range(1, pages_needed + 1):
                # Update status
                self.status_var.set(f"Fetching page {page} of {pages_needed}...")
                
                # Fetch jobs from JSearch API
                new_jobs = self.fetch_jobs_api(job_role, location, remote_only, page)
                
                if not new_jobs:
                    # No more results or error occurred
                    break
                
                all_jobs.extend(new_jobs)
                
                # Don't overwhelm the API
                if page < pages_needed:
                    time.sleep(1)
            
            # Limit to requested number
            all_jobs = all_jobs[:num_results]
            
            # Display results
            self.display_job_results(all_jobs)
            
            self.status_var.set(f"Found {len(all_jobs)} job listings")
            self.job_count_var.set(f"Found {len(all_jobs)} job listings")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.status_var.set(error_msg)
            self.job_count_var.set(error_msg)
            
            # Add detailed error trace to UI
            error_frame = ttk.Frame(self.job_scrollable_frame, relief="ridge", borderwidth=2)
            error_frame.pack(fill="x", padx=5, pady=5, expand=True)
            
            ttk.Label(error_frame, text="Error Details:", font=("", 12, "bold")).pack(anchor="w", padx=10, pady=5)
            
            error_text = ttk.Label(error_frame, text=traceback.format_exc(), foreground="red", 
                                  wraplength=800, justify="left")
            error_text.pack(anchor="w", padx=10, pady=10)
        finally:
            self.root.after(0, lambda: self.search_button.config(state="normal"))
    
    def fetch_jobs_api(self, job_role, location, remote_only=False, page=1):
        """Fetch jobs from JSearch API"""
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
            "X-RapidAPI-Key": self.default_api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=30)
            
            # Check for rate limiting or other errors
            if response.status_code == 429:
                self.status_var.set("API Rate limit exceeded. Please try again later.")
                return []
            
            # Check for any other non-200 responses
            if response.status_code != 200:
                self.status_var.set(f"API Error: Status code {response.status_code}")
                error_details = response.text
                self.root.after(0, lambda: messagebox.showerror("API Error", 
                                                                f"Status: {response.status_code}\n{error_details}"))
                return []
            
            # Process successful response
            data = response.json()
            if "data" in data:
                return data["data"]
            else:
                self.status_var.set("No jobs found or invalid response format.")
                return []
                
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Network error: {str(e)}")
            return []
        except json.JSONDecodeError:
            self.status_var.set("Error: Invalid JSON response from API")
            return []
    
    def fetch_salary_estimate(self):
        """Fetch salary estimate from JSearch API"""
        try:
            job_title = self.salary_job_title.get().strip()
            location = self.salary_location.get().strip()
            experience = self.experience_mapping.get(self.experience_var.get(), "ALL")
            
            # Reset error message
            self.error_var.set("")
            
            url = "https://jsearch.p.rapidapi.com/estimated-salary"
            
            # URL encode the parameters properly
            querystring = {
                "job_title": job_title,
                "location": location,
                "radius": "100",
                "location_type": "ANY",
                "years_of_experience": experience
            }
            
            # Display the URL being requested (for debugging)
            request_url = f"{url}?job_title={quote(job_title)}&location={quote(location)}&radius=100&location_type=ANY&years_of_experience={experience}"
            print(f"Request URL: {request_url}")
            
            headers = {
                "X-RapidAPI-Key": self.default_api_key,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            
            try:
                response = requests.get(url, headers=headers, params=querystring, timeout=30)
                
                # Handle rate limiting
                if response.status_code == 429:
                    error_message = "API Rate limit exceeded. Please try again later."
                    self.root.after(0, lambda: self.error_var.set(error_message))
                    self.status_var.set(error_message)
                    return
                
                # Handle other errors
                if response.status_code != 200:
                    error_message = f"API Error: Status code {response.status_code}"
                    error_details = response.text
                    full_error = f"{error_message}\n\nRequest URL: {request_url}\n\nResponse: {error_details}"
                    self.root.after(0, lambda: self.error_var.set(full_error))
                    self.status_var.set(error_message)
                    return
                
                # Process successful response
                data = response.json()
                if "data" in data and data["data"]:
                    # Update UI with salary data
                    salary_data = data["data"][0]
                    
                    # Format salary values (handle potential missing values)
                    min_salary = f"${int(salary_data.get('min_salary', 0)):,}" if 'min_salary' in salary_data else "--"
                    max_salary = f"${int(salary_data.get('max_salary', 0)):,}" if 'max_salary' in salary_data else "--"
                    median_salary = f"${int(salary_data.get('median_salary', 0)):,}" if 'median_salary' in salary_data else "--"
                    
                    # Update in UI thread
                    self.root.after(0, lambda: self.min_salary_var.set(min_salary))
                    self.root.after(0, lambda: self.max_salary_var.set(max_salary))
                    self.root.after(0, lambda: self.median_salary_var.set(median_salary))
                    
                    # Add source information
                    source = f"Source: {salary_data.get('publisher_name', 'JSearch')} • Last updated: {salary_data.get('last_updated', 'Recently')}"
                    self.root.after(0, lambda: self.salary_source_var.set(source))
                    
                    self.status_var.set("Salary estimate fetched successfully")
                else:
                    no_data_message = "No salary data available for this job and location"
                    self.root.after(0, lambda: self.error_var.set(no_data_message))
                    self.status_var.set(no_data_message)
            
            except requests.exceptions.RequestException as e:
                error_message = f"Network error: {str(e)}"
                self.root.after(0, lambda: self.error_var.set(error_message))
                self.status_var.set(error_message)
                
        except Exception as e:
            error_message = f"Error: {str(e)}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: self.error_var.set(error_message))
            self.status_var.set(f"Error: {str(e)}")
            
        finally:
            self.root.after(0, lambda: self.salary_button.config(state="normal"))
    
    def open_job_link(self, url):
        """Open job URL in default browser"""
        webbrowser.open_new(url)
    
    def display_job_results(self, jobs):
        """Display job results with clickable links"""
        if not jobs:
            no_jobs_label = ttk.Label(self.job_scrollable_frame, text="No job listings found. Try a different search term or location.", wraplength=800)
            no_jobs_label.pack(pady=10, padx=10, anchor="w")
            return
        
        # Update the job count
        self.job_count_var.set(f"Found {len(jobs)} job listings")
        
        for job in jobs:
            # Create frame for job listing
            job_frame = ttk.Frame(self.job_scrollable_frame, relief="ridge", borderwidth=2)
            job_frame.pack(fill="x", padx=5, pady=5, expand=True)
            
            # Extract job details
            title = job.get("job_title", "Unknown Position")
            company = job.get("employer_name", "Unknown Company")
            
            # FIX: Safely handle location data to prevent TypeError
            job_city = job.get("job_city", "")
            job_state = job.get("job_state", "")
            
            # Handle None values for location fields
            if job_city is None:
                job_city = ""
            if job_state is None:
                job_state = ""
                
            location = ""
            if job_city or job_state:
                location = f"{job_city}, {job_state}".strip().rstrip(',').lstrip(',')
            else:
                location = job.get("job_country", "Remote")
                
            job_type = job.get("job_employment_type", "Full-time")
            posted_date = job.get("job_posted_at_datetime_utc", "Recently")
            job_url = job.get("job_apply_link", "")
            
            # Format the date
            try:
                from dateutil import parser
                from datetime import datetime, timezone
                
                date_obj = parser.parse(posted_date)
                now = datetime.now(timezone.utc)
                
                # Calculate days ago
                days_ago = (now - date_obj).days
                if days_ago == 0:
                    posted_date = "Today"
                elif days_ago == 1:
                    posted_date = "Yesterday"
                else:
                    posted_date = f"{days_ago} days ago"
            except:
                # If date parsing fails, keep the original
                pass
            
            # Title with hyperlink
            title_link = ttk.Label(job_frame, text=title, foreground="blue", cursor="hand2", font=("", 12, "bold"))
            title_link.pack(anchor="w", padx=10, pady=(10, 5))
            title_link.bind("<Button-1>", lambda e, url=job_url: self.open_job_link(url))
            
            # Company and location
            ttk.Label(job_frame, text=f"{company} • {location} • {job_type}").pack(anchor="w", padx=10, pady=2)
            
            # Posted date
            ttk.Label(job_frame, text=f"Posted: {posted_date}").pack(anchor="w", padx=10, pady=2)
            
            # Check if salary is included
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
                    salary_label = ttk.Label(job_frame, text=salary_text, font=("", 10, "bold"))
                    salary_label.pack(anchor="w", padx=10, pady=2)
            
            # Description (truncated)
            description = job.get("job_description", "No description available.")
            if len(description) > 300:
                description = description[:300] + "..."
            
            description_text = ttk.Label(job_frame, text=description, wraplength=800, justify="left")
            description_text.pack(anchor="w", padx=10, pady=(5, 10))
            
            # Job link display
            if job_url:
                link_text = ttk.Label(job_frame, text=f"Job URL: {job_url}", foreground="blue", cursor="hand2", wraplength=800)
                link_text.pack(anchor="w", padx=10, pady=(0, 5))
                link_text.bind("<Button-1>", lambda e, url=job_url: self.open_job_link(url))
            
            # Apply button
            apply_button = ttk.Button(
                job_frame, 
                text="Apply Now", 
                command=lambda url=job_url: self.open_job_link(url)
            )
            apply_button.pack(anchor="e", padx=10, pady=(0, 10))

if __name__ == "__main__":
    root = tk.Tk()
    app = JobSearchApp(root)
    
    # Try to set a nice icon and theme if available
    try:
        # Try to use a more modern theme if available
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except:
        pass
    
    try:
        # Try to load an icon
        root.iconbitmap("job_icon.ico")
    except:
        pass
    
    root.mainloop()