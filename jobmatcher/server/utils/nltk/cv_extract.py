from jobmatcher.server.utils.nltk import extract_details

def try_cv(cv_text):
    cv_list = extract_details.extract_skills(cv_text)
    cv_str = ' '.join(str(e) for e in cv_list)
    cv_list = (extract_details.extract_experience(cv_text))
    cv_str += ' '.join(str(e) for e in cv_list)
    return cv_str
