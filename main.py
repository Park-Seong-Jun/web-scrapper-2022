from indeed import extract_indeed_page, extract_indeed_jobs, extract_indeed_last_page


max_indeed_pages = extract_indeed_last_page()

print(extract_indeed_jobs(max_indeed_pages))
