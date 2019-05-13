from jobmatcher.server.modules.user.User import User
from jobmatcher.server.modules.cv.CV import CV
from jobmatcher.server.utils.SOS.skillsExtract import extract_skills
dict_lang_programmimg = {
    "Front-end" : ['javascript', 'angular', 'react',  'html', 'css'],
    "client side" : ['javascript','js','angular', 'react', 'nodejS', 'html', 'css','juery','restful','asp'],  # the same like front end
    "Back-end": ['c','c++','cpp', 'php','python','java','c#', 'javascript', 'js', 'ruby','.net','html','css','asp.net' ],
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
    "robotika":[],
    "web": ['javascript','js','html','css','react'],
    "front end": ['javascript','js','angular', 'react', 'nodejS', 'html', 'css','juery','restful','asp'],
    "client side": [],  # the same like front end
    "back end": ['c','c++','cpp', 'php','python','java','c#', 'javascript', 'js', 'ruby','.net','html','css','asp.net' ],
    "server side": [], # the same like back end
    "data base": ['sql', 'cassandra', 'mongodb', 'firebase', 'oracle','prolog'],
    "security": [], # maybe the same like cyber
    "cyber": ['spoofing','phishing','sniffer','wireshark','putty','namp'],
    "mobile": ['swift','java','c#','ios','android'],
    "game": ['c++','cpp','c#'],
    "desktop": ['.net','azure'],
    "qa": ['test','automation','waterfall','scrum','agile',],
    "devops":['agile','automation','it','collaboration','communication','application','platform','infrastructure'],
    "software": ['development','maintenance','operation', 'testing', 'it system','javascript','js'],
    "development": [],
    "architecture": ['algorithm','platform'],
    "machine learning": [],
    "intelligence": [],
    "big data": [],
    "analyze": [],
    "": []
}


trending = {
    "Front-end": ['React', 'CSS', 'Angular', 'JavaScript', 'Html'],
    "Back-end": ['Flask', 'node.js', 'Python', 'Java', 'PHP', 'Ruby', 'Rails', '.Net'],
    "Full-stack": ['React', 'CSS', 'Angular', 'JavaScript', 'Html', 'Flask', 'node.js', 'Python', 'Java', 'PHP', 'Ruby', 'Rails', '.Net'],
    "DB": ['MySQL', 'mongoDB', 'Oracle', 'SQL', 'SQLite', 'Microsoft SQL Server'],
    "Cyber": ['C', 'C++', 'Python', 'Assembly', 'PHP', 'JavaScript', 'HTML*'],
    "Mobile": ['Swift', 'Python', 'Java', 'JavaScript', 'BuildFire.js', 'HTML5', 'Objective-C', 'C#', 'C++'],
    "QA": ['Python', 'Java', 'C#', 'Perl', 'C', 'C++', 'JavaScript'],
    "Devops": ['Go', 'Python', 'Ruby', 'Scala', 'C', 'Bash', 'Tcl'],
    "Machine-learning": ['R', 'Python', 'Lisp', 'Prolog', 'Java', 'C++', 'JavaScript'],
    "Big data": ['Scala', 'Python', 'R', 'Java', 'Go', '', ''],
    "Game Development": ['C++', 'C#', 'Java', 'Python', 'Lua', 'Objective C', 'JavaScript', 'HTML5', 'Papyrus', 'Cg'],
    "Hardware": ['Pascal', 'Lisp', 'Assembly', 'MATLAB', 'C#', 'Java', 'Python', 'C', 'C++'],
    "Network": ['Python', 'Java', 'C', 'C++', 'C#', 'Perl'],
    "Cloud": ['SQL', 'XML', 'R Math', 'Clojure Math', 'Haskell', 'Erlang', 'Python', 'Go'],
    "Algorithms": ['C#', 'Python', 'R', 'C++', 'MatLab', 'Perl', 'Java'],
    "Data Science": ['R', 'Python', 'Java', 'SQL', 'Julia', 'Scala', 'MatLab', 'TensorFlow', 'JavaScript', 'C#', 'Ruby', 'Perl', 'SAS'],
    "Embedded": ['C', 'C++', 'Java', 'Python', 'Rust', 'Ada', 'Assembly', 'C#'],
    "Artificial Intelligence": ['Python', 'R', 'Lisp', 'Prolog', 'Java', 'C++', 'JavaScript', 'Haskell', 'Julia']

}


def recommendation(user_id):
    print("RECOMMENDATION")
    user = User.objects.get(pk=user_id)
    user_tags = user.tags
    print("user_tags:")
    print(user_tags)
    user_cv = user.cvs[0].text
    skills_list = extract_skills(user_cv)
    print("skills_list")
    print(skills_list)

    result_dict = {}
    for x in user_tags:
        temp = []
        for i in trending[x]:
            if i.lower() not in skills_list:
                temp.append(i)
        result_dict[x] = temp

    # for x in result_dict:
    #     print(result_dict[x][0])


    print("result_dict")
    print(result_dict)
    return result_dict










