import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import pandas as pd
import os
# java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
# os.environ['JAVAHOME'] = java_path
import nltk
from fuzzywuzzy import fuzz
import spacy
from difflib import SequenceMatcher

nltk.download('stopwords')
nltk.download('wordnet')
nlp = spacy.load("en_core_web_sm")  # load the English model - load pre-trained model

STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
            'BACHELOR', 'OF SCIENCE', 'B.SC' , 'BSC'
            ]
#from job
def extract_location_job(str):
    #if have city, replace the comma to space
    #str = re.sub(r'[?|$|.|!|,]', r'', str)
    #str = str.replace(",", " , ")
    #str = str.replace("-"," ")
    #parse_tree = ne_chunk(pos_tag(str.split()), binary=True)  # POS tagging before chunking!
    parse_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(str)), binary=True)  # POS tagging before chunking!

    named_entities = []

    for t in parse_tree.subtrees():
        if t.label() == 'NE' or t.label() == 'GPE' or t.label() == 'PERSON' or t.label() == 'ORGANIZATION':
            named_entities.append(t)
            # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
    # connect name entity to one
    named_entities_str = [" ".join(w for w, t in elt) for elt in named_entities if isinstance(elt, Tree)]

    return named_entities , named_entities_str

#from cv
# def extract_location_cv():
#     st = StanfordNERTagger('C:/Users/eden/Desktop/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
#                            'C:/Users/eden/Desktop/stanford-ner-2018-10-16/stanford-ner.jar')
#
#     # text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'
#     loc = 'Details:' \
#           'Full name: Israel Aviv .' \
#           'Address: Hazait 54, Givat-Shmuel .' \
#           'Mobile: 050-4344936 .' \
#           'Email: chenyair1617@gmail.com .' \
#           'ID: 316178748 .'
#     tokenized_text = word_tokenize(loc)
#     classified_text = st.tag(tokenized_text)
#     data = pd.read_csv('utils/nltk/locations.csv')
#     # extract values
#     location = list(data.columns.values)
#     arr=[]
#     for token in classified_text:
#         if (token[1]=='LOCATION')and not(token[0]=='Israel'):
#             arr.append(token[0])
#         else:
#             if token[0].lower() in location:
#                 # print('-----------------')
#                 # print(token)
#                 if token[0].lower() not in arr:
#                     arr.append(token[0].lower())
#     print(arr)

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    noun_chunks = []
    # print('noun chunk: ')
    for chunk in nlp_text.noun_chunks:  # iterate over the noun chunks in the Doc
        #print(chunk)
        noun_chunks.append(chunk)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    # C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\nltk\\skills.csv
    # for Tal : C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\nltk
    # C:\Users\eden\PycharmProjects\server\job-matcher-server\jobmatcher\server\utils\nltk\skills.csv
    data = pd.read_csv('utils/nltk/skills.csv')
    # extract values
    skills = list(data.columns.values)
    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            # print('-----------------')
            # print(token)
            if token.lower() not in skillset:
                skillset.append(token.lower())

    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            # print('$$$$$$$$$$$$$$$$$$$$$$$')
            # print(token)
            if token.lower() not in skillset:
                skillset.append(token.lower())
    #print(skillset)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                #print('-----------> ' + edu[tex])
                if tex == 'Bachelor':
                    tex = 'B.S'
                    edu[tex] = text + nlp_text[index]
                else:
                    edu[tex] = text + nlp_text[index]

    # :was TO DO to check for job maybe to delete only for job !!! - eden!
    # Extract year
    education = []
    for key in edu.keys():

        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    #print(education)
    return education

def extract_experience(resume_text):
    '''
    Helper function to extract experience from resume text

    :param resume_text: Plain resume text
    :return: list of experience
    '''

    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words]
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('S: {<NNP>+}')
    cs = cp.parse(sent)
    # j=0
    # for i in cs.subtrees():
    #     j+=1
    #     print(j)
    #     print(i)
    #     print(i.label())

    # filter = lambda x: x.label() == 'S'
    # for i in cs.subtrees():
    #     print(filter(i))
    #     print(i)
    #print(cs.label())
    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label()=='S')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))
    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]

    #print(x)
    return x

def partial_ratio(s1, s2):
    """
    Return the ratio of the most similar substring
    as a number between 0 and 100.
    """

    if len(s1) <= len(s2):
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1

    m = SequenceMatcher(None, shorter, longer, autojunk=False)
    blocks = m.get_matching_blocks()

    # each block represents a sequence of matching characters in a string
    # of the form (idx_1, idx_2, len)
    # the best partial match will block align with at least one of those blocks
    #   e.g. shorter = "abcd", longer = XXXbcdeEEE
    #   block = (1,3,3)
    #   best score === ratio("abcd", "Xbcd")
    scores = []
    for (short_start, long_start, _) in blocks:
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]

        m2 = SequenceMatcher(None, shorter, long_substr, autojunk=False)
        r = m2.ratio()
        if r > .995:
            return 100
        else:
            scores.append(r)

    return max(scores) * 100.0

def extract_location(resume_text, match_threshold=90):
    """
    extract locations using fuzzy string matching
    :param resume_text:
    :param match_threshold:
    :return:
    """
    location_matches = []
    # load the locations2 csv file (will be used as the source of comparison)
    # C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\nltk\\locations2.csv
    # C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\nltk\\locations2.csv

    data = pd.read_csv('utils/nltk/locations2.csv')
    locations = list(data.columns.values)
    resume_text = resume_text.lower()
    for location in locations:

        # iterate on all the locations from the csv file and consider the ones above a given threshold as a match
        # ratio = partial_ratio(location.lower(), resume_text)
        # ratio = fuzz.partial_ratio(location.lower(), resume_text)
        ratio = fuzz.token_set_ratio(location.lower(), resume_text)
        if ratio >= match_threshold:
            location_matches.append(location)
    return location_matches

FULL = 'full'
HALF = ['half','part']
STUDENT = 'student'
#get job type as a string and return the type full/part/student and default is full
def extract_type(job_type):
    if FULL in job_type: #first because we decide full will be the default if have a job type for full & half we take the full
        return FULL
    for i in HALF:
        if i in job_type:
            return HALF[0]
    if STUDENT in job_type:
        return STUDENT
    return FULL
