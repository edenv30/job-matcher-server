import requests
from bs4 import BeautifulSoup
#from jobmatcher.server.modules.job.Job import Job
from.job import Job
from googletrans import Translator
import re   # Regular expression operations

def web_scrap(urlJob):
    # urlJob = 'https://www.jobmaster.co.il/jobs/?headcatnum=15&lang=en'
    response = requests.get(urlJob)  # to check for the other pages (checking only the first page) -> to change the URL
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('article')
    # print(jobs)

    listId = check_exist_id()

    for job in jobs:
        id = job.attrs['id']
        if id not in listId:
            jName = translateH2E(job.find(class_='CardHeader').get_text())
            #jLocation = []
            #jLocation.append(translateH2E(job.find(class_='jobLocation').get_text()))
            jLocation=translateH2E(job.find(class_='jobLocation').get_text())
            #jType = []
            #jType.append(translateH2E(job.find(class_='jobType').get_text()))
            jType=translateH2E(job.find(class_='jobType').get_text())
            # jLink
            link = job.find('span').get('onclick')
            if link is not None:
                # print('have link job')
                num = int(re.search(r'\d+', link).group())   # extract number from string with regular exp
                jlinkPopUp = 'https://www.jobmaster.co.il/jobs/checknum.asp?flagShare=' + str(num) + '&lang=en'

                jSalary = translateH2E(job.find(class_='jobSalary').get_text())
                # JDR job D - description R - requirements
                temp = job.find_all(class_='JobItemSubHeader')  # for checkin if Description or Requirements
                jDR = []
                jdrRigth = job.findAll('div', {'style': 'text-align:right'})
                jdrLeft = job.findAll('div', {'style': 'text-align:left'})
                if (jdrRigth != None):
                    for item in jdrRigth:
                        jDR.append(item.get_text())
                if (jdrLeft != None):
                    for item in jdrLeft:
                        jDR.append(item.get_text())

                if (temp[0].get_text() == 'Description'):
                    des = translateH2E(jDR[0])
                else:
                    des = 'no description'
                if (temp[1].get_text() == 'Requirements'):
                    req = translateH2E(jDR[1])
                else:
                    req = 'no requirements'
                # csv_writer.writerow([jName, jLocation, jType, jSalary, jDR[0],jDR[1]])
                # insert into mongoDB:
                jobMongo = Job(
                    identifier=id,
                    role_name=jName,
                    location=jLocation,
                    type=jType,
                    salary=jSalary,
                    description=des,
                    requirements=req,
                    link=jlinkPopUp
                )
                # print('JOB SCARP', id, jName, jLocation, jType, jSalary, des, req, jlinkPopUp)
                jobMongo.save()
                # jExperience(skills,seniority)   - nltk !
            # else:
            #     print('not link job')
            #     jlinkPopUp = 'No contact - no link'
            #     break;


#check if job exist in the data base
def check_exist_id():
    listID = []
    for job in Job.objects:
        listID.append(job['identifier'])
    # print(listID)
    return listID

#translate from hebrew to english
def translateH2E(str):
    translator = Translator()
    res = translator.translate(str, dest='en').text
    return res