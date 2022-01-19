from textwrap import indent
import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr&as_any&as_not&as_ttl&as_cmp&jt=all&st&salary&radius=25&l&fromage=any&limit={LIMIT}&sort&psf=advsrch&from=advancedsearch&vjk=b1ae2fb6f7825a8a"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class":"pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("div", {"class": "heading4 color-text-primary singleLineTitle tapItem-gutter"}).find_all("span")
    title = title[-1].string
    company = html.find("span", {"class": "companyName"})
    location = html.find("div", {"class": "companyLocation"}).string
    job_id = html["data-jk"]
    if company is None:
        company = None
    else:
        company = company.string
    return {
        'title': title, 
        'company': company, 
        'location': location, 
        'link': f"https://kr.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping INDEED page {page}")
        result = requests.get(f"{URL}&start={LIMIT*page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class": "tapItem"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs