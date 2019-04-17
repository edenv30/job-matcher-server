from jobmatcher.server.utils.nltk import extract_details
from jobmatcher.server.modules.job.job import Job

def try_job():
    # skills ='DBA SQL is a leading company in the field of Internet systems development ' \
    #         'In the role of SQL Server programming versions 2008 and later. '\
    #         'Full time work Sunday through Thursday between 9-18 hours without overtime / ' \
    #         'no shifts !! Work in the central region'
    # print(extract_details.extract_skills(skills))
    # education = '5+ years as a Product Manager in web/client environment and enterprise B2BExperience with for elegant B.E. 2013'
    # print(extract_details.extract_education(education))
    # experience = 'of experience five years in c++ and python'
    # print(extract_details.extract_experience(experience))
    exteact_data = {}
    skills = {}
    education = {}
    experience = {}
    jobs = Job.objects
    for j in jobs():
        skills = get_skills(j,skills)
        education = get_education(j,education)
        experience = get_experience(j,experience)
    exteact_data['skills'] = skills
    exteact_data['education'] = education
    exteact_data['experience'] = experience
    #print(exteact_data)
    return exteact_data

def get_skills(job,skills):
    sr = extract_details.extract_skills(job['requirements'])
    sd = extract_details.extract_skills(job['description'])
    skills[job['identifier']] = []
    (skills[job['identifier']]).append(sr)
    (skills[job['identifier']]).append(sd)
    return skills

def get_education(job,education):
    er = extract_details.extract_education(job['requirements'])
    ed = extract_details.extract_education(job['description'])
    education[job['identifier']] = []
    (education[job['identifier']]).append(er)
    (education[job['identifier']]).append(ed)
    return education

def get_experience(job,experience):
    expr = extract_details.extract_experience(job['requirements'])
    expd = extract_details.extract_experience(job['description'])
    experience[job['identifier']] = []
    (experience[job['identifier']]).append(expr)
    (experience[job['identifier']]).append(expd)
    return experience