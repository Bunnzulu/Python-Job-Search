import requests
from bs4 import BeautifulSoup
from math import ceil
from concurrent.futures import ThreadPoolExecutor

def fetch(url):
    response = requests.get(url)
    return response.text

def parse_job_boxes(result):
    jobs = []
    doc = BeautifulSoup(result, "lxml")
    boxes = doc.find_all(class_="clearfix job-bx wht-shd-bx")
    for index, box in enumerate(boxes):
        job_info = {}
        job_title = box.a.text.strip()
        company_title = box.find(class_="joblist-comp-name").text.strip()
        job_skills = box.find(class_="srp-skills").text.replace(' ', '').strip()
        job_link = box.a["href"]
        job_location = box.find("span").text if box.find("span").text else "Not Stated"
        job_info["Title"] = job_title
        job_info["Company"] = company_title
        job_info["Keyskills"] = job_skills
        job_info["Job Link"] = job_link
        job_info["Location"] = job_location
        jobs.append(job_info)
    return jobs

def search_times_jobs(keyword):
    jobs = []
    page = 1
    start_page = 1

    initial_url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={page}&startPage={start_page}"
    initial_result = fetch(initial_url)
    initial_doc = BeautifulSoup(initial_result, "lxml")
    number_of_jobs = int(initial_doc.find(id="totolResultCountsId").text)
    pages = ceil(number_of_jobs / 25)

    urls = [f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={page}&startPage={start_page}"
            for page in range(1, pages + 1)
            for start_page in range(1, ceil(pages / 10) + 1, 10)]

    with ThreadPoolExecutor(max_workers=9999999) as executor:
        results = list(executor.map(fetch, urls))

    for result in results:
        jobs.extend(parse_job_boxes(result))
        
    return jobs
