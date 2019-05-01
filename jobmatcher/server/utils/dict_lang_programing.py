from jobmatcher.server.modules.user.User import User
from jobmatcher.server.modules.cv.CV import CV
from jobmatcher.server.utils.SOS.skillsExtract import extract_skills
dict_lang_programmimg = {
    "web" : ['javascript','js','html','css',],
    "front end" : ['javascript','js','angular', 'react', 'nodejS', 'html', 'css','juery','restful','asp'],
    "client side" : ['javascript','js','angular', 'react', 'nodejS', 'html', 'css','juery','restful','asp'],  # the same like front end
    "back end" : ['c','c++','cpp', 'php','python','java','c#', 'javascript', 'js', 'ruby','.net','html','css','asp.net' ],
    "server side" : ['c','c++','cpp', 'php','python','java','c#', 'javascript', 'js', 'ruby','.net','html','css','asp.net' ], # the same like back end
    "data base" : ['sql', 'cassandra', 'mongodb', 'firebase', 'oracle','prolog'],
    "fullstack" : ['javascript','js','java','c','c++','cpp','python','php','ruby','c#'],
    "security" : ['spoofing','phishing','sniffer','wireshark','putty','namp'],
    "cyber" : ['spoofing','phishing','sniffer','wireshark','putty','namp'],
    "mobile" : ['swift','java','c#','ios','android'],
    "game" : ['c++','cpp','c#','java','perl','assembly','lua'],
    "desktop" : ['.net','azure'],
    "qa" : ['test','automation','waterfall','scrum','agile',],
    "devops" :['agile','automation','it','collaboration','communication','application','platform','infrastructure'],
    "software" : ['development','maintenance','operation', 'testing', 'it system','javascript','js'],
    "hardware":['linux','devalopment'],
    "network":['sdn','automation','json','python','perl'],
    "cloud":['java','j2ee','aws','sql'],
    "development" : ['algorithms','web'],
    "architecture" : ['algorithm','platform'],
    "machine learning" : [],
    "artificial intelligence": [],
    "big data" : [],
    "analyze" : [],
    "robotika":[]
}


def recommendation(user_id):
    user = User.objects.get(id=user_id)
    list_tags=user.tags
    cv = CV.objects.get(user=user.id)
    cv_text=cv.text
    list_skills=extract_skills(cv_text)
    # print(list_skills)
    rec={}
    for i in list_tags:
        tmp = []
        for j in dict_lang_programmimg[i]:
            # print(i,j)
            if j not in list_skills:
                tmp.append(j)
        rec[i]=tmp
    return rec


