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


def extract_indeed_last_page():
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


def extract_indeed_jobs(last_page):
    jobs = []
    # for n in range(last_page):
    result = requests.get(f"{URL}&start = {0*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class", "resultWithShelf"})
    for result in results:
        title = result.find("div", "singleLineTitle").find(
            "a").find("span").string
        company = result.find("div", "companyInfo").find(
            "span", {"class", "companyName"}).string
        print(title, company)

    return jobs
