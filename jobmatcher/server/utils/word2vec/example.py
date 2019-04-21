# # import io
# # import panda as pd
# # import nltk
# # import gensim
# # from gensim import corpora,models,similarities
# # GLOVE WORD2VEC
#
# from gensim.models import word2vec
# import logging
#
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# sentences = word2vec.Text8Corpus('C:/Users/eden/PycharmProjects/server/job-matcher-server/jobmatcher/server/utils/word2vec/text8')
# model = word2vec.Word2Vec(sentences, size=200)
#
# print(model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1))
