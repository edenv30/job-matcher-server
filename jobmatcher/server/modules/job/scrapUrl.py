import requests
from bs4 import BeautifulSoup
from jobmatcher.server.modules.job.jobMaster import web_scrap

def scarpUrl():
    urlJob = 'https://www.jobmaster.co.il/jobs/?headcatnum=15&lang=en'
    response = requests.get(urlJob)  # to check for the other pages (checking only the first page) -> to change the URL
    soup = BeautifulSoup(response.text, 'html.parser')

    urlList = []
    urlList.append(urlJob)
    for link in soup.find_all(class_='paging'):
        #print('https://www.jobmaster.co.il'+link.get('href'))
        page = link.get('href')
        url = 'https://www.jobmaster.co.il'+ page
        urlList.append(url)

    for i in range (urlList.__len__() - 6):   # len -1 because in jobMaster the last paging return to page#2
        web_scrap(urlList[i])

    print(urlList)