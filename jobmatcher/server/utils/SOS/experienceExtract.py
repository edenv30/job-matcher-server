from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

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
    j=0
    for i in cs.subtrees():
        j+=1
        print(j)
        print(i)
        print(i.label())

    filter = lambda x: x.label() == 'S'
    for i in cs.subtrees():
        print(filter(i))
        print(i)
    #print(cs.label())
    test = []

    for vp in list(cs.subtrees(filter=lambda x: x.label()=='S')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))
    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]

    print(x)
    return x