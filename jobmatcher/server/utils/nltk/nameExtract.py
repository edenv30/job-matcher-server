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

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        print(span.text)

    for match_id, start, end in matches2:
        span = nlp_text[start:end]
        print(span.text)
    return

