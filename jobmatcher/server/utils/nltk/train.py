import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names


def word_feats(words):
    return dict([(word, True) for word in words])

def test():
    positive_vocab = ['awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great','like', 'beauty' ,':)']
    negative_vocab = ['bad', 'terrible', 'useless', 'hate', ':(']
    neutral_vocab = ['movie', 'the', 'sound', 'was', 'is', 'actors', 'did', 'know', 'words', 'not']

    positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
    negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
    neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

    train_set = negative_features + positive_features + neutral_features
    print(train_set)
    classifier = NaiveBayesClassifier.train(train_set)

    # Predict
    neg = 0
    pos = 0
    sentence = "Awesome and fantastic movie, beauty like I liked it love nice good beautifule pretty"
    sentence = sentence.lower()
    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(word_feats(word))
        print(word +  ': ' + classResult)
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    print('Positive: ' + str(float(pos) / len(words)))
    print('Negative: ' + str(float(neg) / len(words)))