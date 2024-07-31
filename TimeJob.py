import aiohttp
import asyncio
from bs4 import BeautifulSoup
from math import ceil

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(session, urls):
    tasks = []
    for url in urls:
        tasks.append(fetch(session, url))
    results = await asyncio.gather(*tasks)
    return results

async def SearchTimesJobs(keyword):
    JOBS = {}
    Page = 1
    StartPage = 1

    initial_url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={Page}&startPage={StartPage}"
    async with aiohttp.ClientSession() as session:
        initial_result = await fetch(session, initial_url)
        initial_doc = BeautifulSoup(initial_result, "html.parser")
        Number_of_Jobs = int(initial_doc.find(id="totolResultCountsId").text)
        Pages = ceil(Number_of_Jobs / 25)
        
        urls = [f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={page}&startPage={start_page}"
                for page in range(1, Pages + 1)
                for start_page in range(1, ceil(Pages / 10) + 1, 10)]
        
        results = await fetch_all(session, urls)
        
        for page_index, result in enumerate(results):
            doc = BeautifulSoup(result, "lxml")
            Boxes = doc.find_all(class_="clearfix job-bx wht-shd-bx")
            for index, Box in enumerate(Boxes):
                JobInfo = {}
                Job_Title = Box.a.text.strip()
                Company_Title = Box.find(class_="joblist-comp-name").text.strip()
                Job_Skills = Box.find(class_="srp-skills").text.replace(' ', '').strip()
                Job_Link = Box.a["href"]
                Job_Location = Box.find("span").text if Box.find("span").text else "Not Stated"
                JobInfo["Title"] = Job_Title
                JobInfo["Company"] = Company_Title
                JobInfo["Keyskills"] = Job_Skills
                JobInfo["Job Link"] = Job_Link
                JobInfo["Location"] = Job_Location
                JOBS[f"Job{page_index}{index}"] = JobInfo
                
    return JOBS


keyword = "python"
jobs = asyncio.run(SearchTimesJobs(keyword))
print(jobs)
