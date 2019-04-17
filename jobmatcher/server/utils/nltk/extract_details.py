import pandas as pd
import spacy
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
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

    # C:\Users\Tal\PycharmProjects\server\jobmatcher\server\utils\nltk
    data = pd.read_csv(
        'C:\\Users\\Tal\\PycharmProjects\\server\\jobmatcher\\server\\utils\\nltk\\skills.csv')
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

    # to check for job maybe to delete only for job !!! - eden!
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