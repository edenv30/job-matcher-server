from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from jobmatcher.server.modules.job.job import Job
import re

#take attrs from job collection and extract with nltk
def take_collection():
    jobs = Job.objects
    for j in jobs():
        loc=extract_location(j["location"])
        #print(loc[0], loc[1]) 0 - tree 1 - list
        print('location list: ')
        print(loc[1])
        # print('tree location: ')
        # print(loc[0])
        #typej=extract_type(j["type"])
        #print(typej)

def extract_location(str):
    #if have city, replace the comma to space
    #str = re.sub(r'[?|$|.|!|,]', r'', str)
    #str = str.replace(",", " , ")
    #str = str.replace("-"," ")
    #parse_tree = ne_chunk(pos_tag(str.split()), binary=True)  # POS tagging before chunking!
    parse_tree = ne_chunk(pos_tag(word_tokenize(str)), binary=True)  # POS tagging before chunking!

    named_entities = []

    for t in parse_tree.subtrees():
        if t.label() == 'NE' or t.label() == 'GPE' or t.label() == 'PERSON' or t.label() == 'ORGANIZATION':
            named_entities.append(t)
            # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
    # connect name entity to one
    named_entities_str = [" ".join(w for w, t in elt) for elt in named_entities if isinstance(elt, Tree)]

    return named_entities , named_entities_str

# def extract_type(str):
#     str = str.replace(",", " , ")
#     parse_tree = pos_tag(word_tokenize(str))
#     print(parse_tree)

