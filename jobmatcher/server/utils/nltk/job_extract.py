from jobmatcher.server.utils.nltk import extract_details

def try_job():
    skills ='DBA SQL is a leading company in the field of Internet systems development ' \
            'In the role of SQL Server programming versions 2008 and later. '\
            'Full time work Sunday through Thursday between 9-18 hours without overtime / ' \
            'no shifts !! Work in the central region'
    print(extract_details.extract_skills(skills))
    education = '5+ years as a Product Manager in web/client environment and enterprise B2BExperience with for elegant B.E. 2013'
    print(extract_details.extract_education(education))
    experience = 'of experience five years in c++ and python'
    print(extract_details.extract_experience(experience))