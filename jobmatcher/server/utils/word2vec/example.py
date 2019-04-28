# from gensim.models import word2vec
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# sentences = word2vec.Text8Corpus('C:\\Users\\eden\\PycharmProjects\\server\\job-matcher-server\\jobmatcher\\server\\utils\\word2vec\\text8')
# model = word2vec.Word2Vec(sentences, size=200)
#
# print('example file')
# print(model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1))
# import bs4 as bs
# import urllib.request
# import re
# import nltk
# from gensim.models import Word2Vec
#
# scrapped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
# article = scrapped_data.read()
#
# parsed_article = bs.BeautifulSoup(article,'lxml')
#
# paragraphs = parsed_article.find_all('p')
#
# article_text = ""
#
# for p in paragraphs:
#     article_text += p.text
#
# # Cleaing the text
# processed_article = article_text.lower()
# processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
# processed_article = re.sub(r'\s+', ' ', processed_article)
#
# # Preparing the dataset
# all_sentences = nltk.sent_tokenize(processed_article)
#
# all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
#
# # Removing Stop Words
# from nltk.corpus import stopwords
# for i in range(len(all_words)):
#     all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
#
#
# word2vec = Word2Vec(all_words, min_count=2)
# vocabulary = word2vec.wv.vocab
# print(vocabulary)
# v1 = word2vec.wv['artificial']
# print(v1)
# sim_words = word2vec.wv.most_similar('intelligence')
# print(sim_words)

from gensim.models import Word2Vec

def example():
	# define training data
	sentences = [['python', 'is', 'the', 'first', 'language', 'for', 'server','side'],
				['html', 'is', 'the', 'second','language', 'web','side'],
				['css','is', 'the', 'third','language', 'web','side'],
				['python', 'work', 'for','server','side'],
				['java', 'is', 'programming', 'language','works','with','']]
	# train model
	model = Word2Vec(sentences, min_count=1)
	# summarize the loaded model
	# print('model')
	# print(model)
	# summarize vocabulary
	words = list(model.wv.vocab)
	# print('words')
	# print(words)
	# access vector for one word
	# print(model['sentence'])
	# save model
	model.save('model.bin')
	# load model
	new_model = Word2Vec.load('model.bin')
	# print('new_model')
	# print(new_model)

	print(model.similarity('python','server'))
	print(model.similarity('python','web'))


	# X = model[model.wv.vocab]
	# print('X')
	# print(X)


