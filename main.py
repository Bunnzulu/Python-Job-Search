from bs4 import BeautifulSoup
import requests


keyword = "python"
Page = 1


url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={Page}&startPage=1"
result = requests.get(url).text

doc = BeautifulSoup(result,"html.parser")

Boxes = doc.find_all(class_ = "clearfix job-bx wht-shd-bx")

for Box in Boxes:
    print(f"Title: {Box.a.text.strip()}")
    print(f"Company: {Box.find(class_="joblist-comp-name").text.strip()}")
    print("-----------")