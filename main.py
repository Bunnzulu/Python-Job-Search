from bs4 import BeautifulSoup
import requests
from math import ceil


keyword = "python" #Job keyword you want to search
Page = 1
StartPage = 1


url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={Page}&startPage={StartPage}"
result = requests.get(url).text

doc = BeautifulSoup(result,"html.parser")

Boxes = doc.find_all(class_ = "clearfix job-bx wht-shd-bx")

Number_of_Jobs = int(doc.find(id = "totolResultCountsId").text)

Pages = ceil(Number_of_Jobs/25)

# for Box in Boxes:
#     Job_Title = Box.a.text.strip()
#     Company_Title = Box.find(class_="joblist-comp-name").text.strip()
#     Job_Skills = Box.find(class_="srp-skills").text.replace(' ','').strip()
#     Job_Link = Box.a["href"]
#     if Box.find("span").text == "": Job_Location = "Not Stated"
#     if Box.find("span").text != "": Job_Location = Box.find("span").text
#     print(f"Title: {Job_Title}")
#     print(f"Company: {Company_Title}")
#     print(f"Keyskills: {Job_Skills}")
#     print(f"Job Link: {Job_Link}")
#     print(f"Location: {Job_Location}")
#     print("-----------")