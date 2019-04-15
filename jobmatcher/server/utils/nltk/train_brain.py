# import nltk.classify.util
# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import names
#
#
# def word_feats(words):
#     return dict([(word, True) for word in words])
#
# def test():
#     lang_pog_vocab = ['react', 'angular', 'java', 'c', 'c++', 'python' , 'sql' ]
#     location_vocab = ['israel', 'Ono Valley', 'usa', 'new york', 'canada' ,'ashdod' , 'ofaqim']
#     role_vocab = ['db', 'qa', 'cyber', 'development']
#
#     lang_pog_features = [(word_feats(pos), 'lan') for pos in lang_pog_vocab]
#     location_features = [(word_feats(neg), 'loc') for neg in location_vocab]
#     role_features = [(word_feats(neu), 'rol') for neu in role_vocab]
#
#     train_set = lang_pog_features + location_features  + role_features
#     print(train_set)
#     classifier = NaiveBayesClassifier.train(train_set)
#
#     # Predict
#     neg = 0
#     pos = 0
#     sentence = "DBA SQL is a leading company in the field of Internet systems development. In the role of SQL Server programming versions 2008 and later. Full time work Sunday through Thursday between 9-18 hours without overtime / no shifts !! Work in the central region"
#     sentence = sentence.lower()
#     words = sentence.split(' ')
#     for word in words:
#         classResult = classifier.classify(word_feats(word))
#         print(word +  ': ' + classResult)
#     #     if classResult == 'lan':
#     #         neg = neg + 1
#     #     if classResult == 'loc':
#     #         pos = pos + 1
#     #
#     # print('languge: ' + str(float(pos) / len(words)))
#     # print('location: ' + str(float(neg) / len(words)))

from nltk import NaiveBayesClassifier as nbc
from nltk.tokenize import word_tokenize
from itertools import chain

def test():
    training_data = [('Software developer in C ++', 'rol'),
    ('dba man', 'rol'),
    ('write some languages','rol'),
    ('WEB Client Product Manager.', 'rol'),
    ('Requires a Full Stack Web Developer.', 'rol'),
    ('server side', 'rol'),
    ('client side', 'rol'),
    ('python sql mongodb java', 'lang'),
    ('matlab javascript ', 'lang'),
    ('react cpp angular php html ', 'lang'),
    ('new york', 'loc'),
    ('tel aviv','loc'),
    ('dimona', 'loc'),
    ('berlin','loc'),
    ('brooklyn','loc')]

    vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
    print(vocabulary)
    print();
    feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
    #print(feature_set)
    for j in feature_set:
        if (feature_set[1] == True):
            print(feature_set[0])
    print();
    classifier = nbc.train(feature_set)

    #test_sentence = "i have a experience in client side develop"
    #test_sentence = 'i know to writing in python'
    test_sentence = 'have skills python'
    featurized_test_sentence =  {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary}
    print(featurized_test_sentence)
    print();
    print ("test_sent:",test_sentence)
    print();
    print ("tag:",classifier.classify(featurized_test_sentence))