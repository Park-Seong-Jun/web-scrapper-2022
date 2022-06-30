import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"


def extract_indeed_page(URL):
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {'class': "pagination"})

    pages = pagination.find_all("a")

    page = [page.string for page in pages[:-1]]

    current_last_page = page[-1]

    return int(current_last_page)


def get_last_page():
    LIMIT = 50
    URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

    last_indeed_page = extract_indeed_page(URL)
    current_indeed_page = last_indeed_page - 2

    while True:
        if current_indeed_page == last_indeed_page - 2:
            current_indeed_page = last_indeed_page
            URL = f"{URL}&start={50*(last_indeed_page-1)}"
            last_indeed_page = extract_indeed_page(URL)
            URL = URL.replace(f"&start={50*(current_indeed_page-1)}", "")
        elif last_indeed_page == current_indeed_page + 1:
            max_indeed_pages = current_indeed_page + 2
            break
        elif last_indeed_page == current_indeed_page - 2:
            max_indeed_pages = current_indeed_page
            break
        elif last_indeed_page == current_indeed_page - 1:
            max_indeed_pages = current_indeed_page + 1
            break
    return max_indeed_pages


def extract_jobs(soup):
    title = soup.find("div", "singleLineTitle").find(
        "a").find("span").string
    company = soup.find("div", "companyInfo").find(
        "span", {"class", "companyName"}).string
    location = soup.find("div", "companyLocation").string
    job_id = soup.find("a")["data-jk"]
    return {'title': title, 'company': company, 'location': location, 'apply_link': f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&vjk={job_id}"}


def extract_page(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start = {0*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class", "resultWithShelf"})
        for result_page in results:
            job = extract_jobs(result_page)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_page(last_page)
    return jobs
