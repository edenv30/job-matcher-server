from nltk.tokenize import sent_tokenize,word_tokenize
import warnings
import gensim
from gensim.models import Word2Vec

def testFunc():
    # TODO: C:\Users\Tal\Desktop

    #  Reads ‘alice.txt’ file
    sample = open("C:\\Users\\Tal\\Desktop\\alice.txt", "r")
    s = sample.read()

    # Replaces escape character with space
    f = s.replace("\n", " ")

    data = []

    # iterate through each sentence in the file
    for i in sent_tokenize(f):
        temp = []

        # tokenize the sentence into words
        for j in word_tokenize(i):
            temp.append(j.lower())

        data.append(temp)

    # Create CBOW model
    model1 = gensim.models.Word2Vec(data, min_count=2, size=100, window=5)
    model2 = gensim.models.Word2Vec(data, min_count=2, size=100, window=5)

    print("Cosine similarity between 'web' " +
          "and 'javascript' - CBOW : ",
          model1.similarity('web', 'javascript'))

    print("Cosine similarity between 'web' " + "and 'python' - CBOW : ",
          model2.similarity('web', 'python'))

