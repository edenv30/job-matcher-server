import pandas as pd
import spacy

# load pre-trained model
nlp = spacy.load("en_core_web_sm")  # load the English model
#noun_chunks = nlp.noun_chunks

def extract_skills(resume_text):
     nlp_text = nlp(resume_text)
     noun_chunks = []
     # print('noun chunk: ')
     for chunk in nlp_text.noun_chunks:  # iterate over the noun chunks in the Doc
         # print(chunk)
         noun_chunks.append(chunk)
     # removing stop words and implementing word tokenization
     tokens = [token.text for token in nlp_text if not token.is_stop]

     # reading the csv file

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
     # print(skillset)
     return skillset
     # return [i.capitalize() for i in set([i.lower() for i in skillset])]

# # import spacy
# # # loading the model
# # nlp = spacy.load('en_core_web_lg')
# #
# # def extract_skills():
# #     doc = nlp(u'"John Smith is lookin for Apple ipod"')
# #     # creating the filter list for tokens that are identified as person
# #     fil = [i for i in doc.ents if i.label_.lower() in ["person"]]
# #     # looping through noun chunks
# #     for chunk in doc.noun_chunks:
# #         # filtering the name of the person
# #         if chunk not in fil:
# #             print(chunk.text)
#
#
