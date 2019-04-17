# -*- coding: utf-8 -*-
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
os.environ['JAVAHOME'] = java_path
def stan():
    sentence = u"Twenty miles east of Reno, Nev., " \
               "where packs of wild mustangs roam free through " \
               "the parched landscape, Tesla Gigafactory 1 " \
               "sprawls near Interstate 80."
    loc = 'Sr. Specialist, IT Administration T-Mobile tel-aviv eden, Bellevue, USA T-Mobile arad Inc is the third largest dimona company in the United States that employees over 51,000 across the states. I have worked in several T-Mobile Engineering offices at the corporate location working break fix issues on over 500 plus engineers laptop and desktops, in buildings containing well over 1000 people. Assisting multiple departments seeing their projects to completion. Trouble shooting networking, software, hardware problems. Either solving the issue alone or involving other teams like the Exchange or Server team for further assistance. ' \
              'Configuring and trouble shooting MAC Books on the Domain for engineers supporting the retail environment!' \
             ' Beer sheva 15 plus retail stores with their computer equipment issues'
    loca = 'Tel-Aviv and Petah-Tikva, Ono-Valley and Givat-Shmuel, Ness-Ziona, Rishon-Lezion, Ramat-Gan and Givattayim'
    loc = 'Tel Aviv, Petah Tikva, Ono Valley and Givat Shmuel, Ness Ziona, Rishon Lezion, Ramat Gan and Givattayim'
    loc = 'Tel Aviv, Israel | M +972- 52-3281614| tolmamal@gmail.com'
    #jar = './stanford-ner-tagger/stanford-ner.jar'
    jar='C:/Users/eden/Desktop/stanford-ner-2018-10-16/stanford-ner-2018-10-16/stanford-ner.jar'
    #model = './stanford-ner-tagger/ner-model-english.ser.gz'
    model='C:/Users/eden/Desktop/stanford-ner-2018-10-16/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz'
    # Prepare NER tagger with english model
    ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

    # Tokenize: Split sentence into words
    words = nltk.word_tokenize(loc)

    # Run NER tagger on words
    print(ner_tagger.tag(words))