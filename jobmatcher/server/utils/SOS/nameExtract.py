import spacy
from spacy.matcher import Matcher

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
matcher2=Matcher(nlp.vocab)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    pattern2=[{'POS':'PROPN'}]

    matcher.add("NAME", None, pattern)
    matcher2.add("LOCATION",None,pattern2)

    matches = matcher(nlp_text)
    matches2 = matcher2(nlp_text)
    for token in nlp_text:
        print('The token')
        #print(token.lemma_)
        #print(token.pos_)
        print(token.text + '   ' + token.tag_)
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, pattern)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        print(span.text)

    for match_id, start, end in matches2:
        span = nlp_text[start:end]
        print(span.text)
    return


# import spacy
#
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
#
# def extract_name():
#     for token in doc:
#         print('The token')
#         print(token)
#         print(token.text)
#         print(token.lemma_)
#         print(token.pos_)
#         print(token.tag_)
#         print(token.dep_)
#         print(token.shape_)  # num lemma characters ? X
#         print(token.shape_[0])
#         print(token.is_alpha) #if all character alpahbeit return true if not false
#         print(token.is_stop) # if can stop sentence with word = False else True
#         #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#                 #token.shape_, token.is_alpha, token.is_stop)

# import spacy
# from spacy.matcher import Matcher
#
# nlp = spacy.load("en_core_web_sm")
# matcher = Matcher(nlp.vocab)
# Add match ID "HelloWorld" with no callback and one pattern
# def extract_name():
#     pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
#     matcher.add("HelloWorld", None, pattern)
#
#     doc = nlp(u"Hello, world! Hello world!")
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         print(match_id)
#         print(start)
#         print(end)
#         string_id = nlp.vocab.strings[match_id]  # Get string representation
#         span = doc[start:end]  # The matched span
#         print(match_id, string_id, start, end, span.text)
