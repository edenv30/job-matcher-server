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

    for i in range (urlList.__len__() - 9):   # len -1 because in jobMaster the last paging return to page#2
        print(i)
        web_scrap(urlList[i])

    # print(urlList)


def scrape_cities():
    # scrape cities and save into locations.csv
    url = "http://en.netzah.org/"
    import requests
    response = requests.get(url)  # to check for the other pages (checking only the first page) -> to change the URL
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    locations = []
    for link in soup.find_all('a'):
        location = link.text
        if location and str(location) and len(str(location)):
            locations.append(location)

    import csv
    with open('locations.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(locations)
