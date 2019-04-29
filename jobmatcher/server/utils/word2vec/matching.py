from gensim.models import Word2Vec, KeyedVectors
import spacy
nlp = spacy.load('en_core_web_sm')
import numpy as np
from scipy import spatial
from jobmatcher.server.modules.job.job import Job
from jobmatcher.server.modules.cv.CV import CV
from jobmatcher.server.utils.nltk import job_extract , cv_extract
import pandas as pd


#Next, we define a function to parse the documents (CVs) and save the word embeddings as follows:
#def preprocess_training_data1(dir_cvs, dir_model_name):
def build_vocab(jobs):
    # jobs=get_jobs_from_db()
    alltext = ''
    for k,v in jobs.items():
       alltext+= ' ' + v
    alltext = alltext.lower()
    vector = []
    doc = nlp(alltext)

    for token in doc:
        temp = []
        # if token.tag_ == 'NN' or token.tag_ == 'VB':
        temp.append(token.lemma_)
        vector.append(temp)
    # adding the skills file and the edcucation to the vocabulary
    data = pd.read_csv('C:\\Users\\eden\\PycharmProjects\\server\\job-matcher-server\\jobmatcher\\server\\utils\\nltk\\skills.csv')
    skills = nlp(str(data.columns.values))
    for s in skills:
        if s.lemma_ not in vector:
            vector.append(s.lemma_)
    education = nlp(('BE B.E. B.E BS B.S ME M.E M.E. MS M.S BTECH B.TECH M.TECH MTECH SSC HSC CBSE ICSE X XII BACHELOR' \
                'OF SCIENCE B.SC BSC').lower())
    for i in education:
        if i.lemma_ not in vector:
            vector.append(i.lemma_)

    global model
    model = Word2Vec(vector, size=200, window=5, min_count=1, workers=4)
    # global model1
    # model1 = model
    # global model2
    # model2 = model


#@app.route('/find/', methods=['GET'])
def avg_vec4cv(cv_text):
    # #data = request.args.get('value')
    # cv = CV.objects[0]
    # data = cv['text']
    data = cv_text
    w2v = []
    w2v_value = []
    data = data.lower()
    doc = nlp(data)
    # dataExtract=cv_extract.try_cv(data)
    # doc = nlp(dataExtract)
    for token in doc:
        if token.lemma_ in model.wv.vocab:
            w2v.append(model.wv[token.lemma_])
            w2v_value.append(token.lemma_)
        else:
            if token.lemma_ .lower() in model.wv.vocab:
                w2v.append(model.wv[token.lemma_ .lower()])
                w2v_value.append(token.lemma_ .lower())


    Q_w2v = np.mean(w2v, axis=0)
    return Q_w2v

def get_jobs_from_db():
    jobsDB = Job.objects
    jobs = {}
    for j in jobsDB:
        jobs[j['identifier']] = j['type'] + ' ' + j['description'] + ' ' + j['requirements']
    return jobs



def match_jobs2cv(cv_text):
    jobs=get_jobs_from_db()
    build_vocab(jobs)
    Q_w2v = avg_vec4cv(cv_text)
    # Example of document represented by average of each document term vectors.
    D_w2v = {}

    for key,val in jobs.items():
        w2v = []
        data = val.lower()
        doc = nlp(data)
        for token in doc:
            if token.lemma_ in model.wv.vocab:
                w2v.append(model.wv[token.lemma_])
            else:
                if token.lemma_.lower() in model.wv.vocab:
                    w2v.append(model.wv[token.lemma_.lower()])
        D_w2v[key] = np.mean(w2v, axis=0),val

    # Make the retrieval using cosine similarity between query and document vectors.
    retrieval = {}
    for key, val in D_w2v.items():
        retrieval[key] = 1 - spatial.distance.cosine(Q_w2v, val[0])
        # print(retrieval[key])
        # print(val[1])
    # print(retrieval)
    # TODO: to make if the precent of the job up than __% ?
    jobsss = {}
    for k,v in retrieval.items():
        if v > 0.7:
            jobsss[k] = v

    return  jobsss


def get_list_matching_job(dic):
    job_score = {}
    for k , v in dic.items():
        job = Job.objects.get(identifier=k)
        j_role = job.role_name
        j_link = job.link
        job_score[k] =((j_role,j_link,v))

    return job_score