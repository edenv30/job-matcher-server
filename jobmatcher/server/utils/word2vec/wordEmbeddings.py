from gensim.models import Word2Vec, KeyedVectors
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy import spatial
from sklearn import decomposition
import matplotlib.pyplot as plt

from jobmatcher.server.utils.pattern import text



# def read_All_CV(filename):
#     text = textract.process(filename)
#     return text.decode('utf-8')


allText = " Chris Ware 789 E 901 N , Salt Lake City, UT 11111 E: cwse@fastmail.com P: 555-234-2345" \
    "Professional Summary" \
    "Experienced software engineer with a passion for developing innovative programs that expedite the efficiency and effectiveness of organizational success. Well-versed in technology and writing code to create systems that are reliable and user-friendly. Skilled leader who has the proven ability to motivate, educate, and manage a team of professionals to build software programs and effectively track changes. Confident communicator, strategic thinker, and innovative creator to develop software that is customized to meet a company’s organizational needs, highlight their core competencies, and further their success. " \
    "Skills" \
    "-Well-versed in software tools including HTML, JavaScript, CSS, BackBone and JQuery, among others. -Skilled at reading and writing code using viable inputs and outputs after accurate assessment of pre- and post-conditions. -Experienced at designing unit tests to measure the effectiveness of software programs, backend services, and user interfaces. -Confident problem-solving abilities to overcome glitches with creative solutions that are strategically designed to last long-term. -Strong communication skills and the ability to listen carefully to user feedback to determine modifications for optimal user-function." \
    "Work Experience" \
    "Software Engineer-April 2013 – present Rav Industries" \
    "Developed and designed three critical software programs for financial tracking and reporting." \
          "Optimized user effectiveness by creating a detailed feedback queue for users to discuss functionality, convenience, and effectiveness." \
          "Oversee a team of four software developers and lead weekly discussions to brainstorm ideas in software development and to track changes made in existing programs." \
    "Software Developer-February 2008 – April 2013 Brac Inc." \
    "Participated in creating scalable systems for three primary departments, including human resources, marketing, and supply chain." \
          "Ran monthly unit tests to determine software effectiveness and mend broken links or glitches in the system." \
          "Gave quarterly reports to executive management regarding current developments, and tracked changes in existing software." \
        "Education Internship2010-2011"\
    "Estes Corp. Salt Lake City Utah Bachelor of Science 2010 in Computer Engineering 2010" \
          "University of Utah Salt Lake City Utah"


def preprocess_training_data1():

    s = text.parsetree('The cat sat on the mat.', relations=True, lemmata=True)
    print(s)

    # result = es.parsetree('The cat sat on the mat.', relations=True, lemmata=True)
    #
    # s = en.parse('The cat sat on the mat.', relations=True, lemmata=True)
    #
    #
    #
    # print(s)



    # dircvs = [join(dir_cvs, f) for f in listdir(dir_cvs) if isfile(join(dir_cvs, f))]
    # alltext = ' '
    # for cv in dircvs:
    #     yd = read_All_CV(cv)
    #     alltext += yd + " "

    # alltext = allText.lower()
    # vector = []
    # for sentence in es.parsetree(alltext, tokenize=True, lemmata=True, tags=True):
    #     temp = []
    #     for chunk in sentence.chunks:
    #         for word in chunk.words:
    #             if word.tag == 'NN' or word.tag == 'VB':
    #                 temp.append(word.lemma)
    #     vector.append(temp)
    # global model
    # model = Word2Vec(vector, size=200, window=5, min_count=3, workers=4)
    # # model.save(dir_model_name)
    #
    # print("model:")
    # print(model)