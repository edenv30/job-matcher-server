from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import pandas as pd

import os
java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path
def extract_location():
    st = StanfordNERTagger('C:/Users/eden/Desktop/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                           'C:/Users/eden/Desktop/stanford-ner-2018-10-16/stanford-ner.jar')

    # text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'
    loc = 'Details:' \
          'Full name: Israel Aviv .' \
          'Address: Hazait 54, Givat-Shmuel .' \
          'Mobile: 050-4344936 .' \
          'Email: chenyair1617@gmail.com .' \
          'ID: 316178748 .'
    tokenized_text = word_tokenize(loc)
    classified_text = st.tag(tokenized_text)
    data = pd.read_csv('utils/nltk/locations.csv')
    # extract values
    location = list(data.columns.values)
    arr=[]
    for token in classified_text:
        if (token[1]=='LOCATION')and not(token[0]=='Israel'):
            arr.append(token[0])
        else:
            if token[0].lower() in location:
                # print('-----------------')
                # print(token)
                if token[0].lower() not in arr:
                    arr.append(token[0].lower())
    print(arr)

