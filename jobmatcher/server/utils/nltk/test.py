import nltk
from nltk.corpus import treebank
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#nltk.download('treebank')
#nltk.download('brown')
#from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def test():
    text = "location , role , skills , experience "
    lang = "react , c++ , c , angular, html , python , java , java script "
    s = nltk.pos_tag(nltk.word_tokenize(lang))
    print(s)

    sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good brooklyn dimona israel ."
    # Tokenize the text
    tokens = nltk.word_tokenize(sentence)
    print(tokens)
    # Tag the text
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    # Identify named entities
    entities = nltk.chunk.ne_chunk(tagged)
    print(entities)
    # Display a parse tree:
    t = treebank.parsed_sents('wsj_0001.mrg')[0]
    t.draw()
    # text = nltk.pos_tag(nltk.word_tokenize("And now for something completely different"))
    # print(text)
    # # print(nltk.corpus.brown.words())
    # text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
    # print(text.similar('woman'))

    # text = "tel aviv ramat gan and dimona"
    # tokens = nltk.word_tokenize(text)
    # print(tokens)
    # tag = nltk.pos_tag(tokens)
    # print(tag)
    # ent = nltk.chunk.ne_chunk(text, binary=True)
    # print(ent)
    # text = "WASHINGTON -- new york In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."
    # #text2 = "Ramat Gan and Givatayim"
    # chunked = ne_chunk(pos_tag(word_tokenize(text)))
    # #print(chunked)
    # continuous_chunk = []
    # current_chunk = []
    # for i in chunked:
    #     if type(i) == Tree:
    #         current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    #         print(current_chunk)
    #     elif current_chunk:
    #         named_entity = " ".join(current_chunk)
    #         if named_entity not in continuous_chunk:
    #             continuous_chunk.append(named_entity)
    #             current_chunk = []
    #     else:
    #         continue
    # print(current_chunk)

    # my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."
    # my_sent = "Ramat Gan and Givatayim , Ono Valley and Givat Shmuel"
    # parse_tree = nltk.ne_chunk(nltk.tag.pos_tag(my_sent.split()), binary=True)  # POS tagging before chunking!
    # #print(parse_tree)
    # named_entities = []
    #
    # for t in parse_tree.subtrees():
    #     if t.label() == 'NE':
    #         named_entities.append(t)
    #         # named_entities.append(list(t))  # if you want to save a list of tagged words instead of a tree
    #
    # print (named_entities)
    # named_entities_str = [ " ".join(w for w, t in elt) for elt in named_entities if isinstance(elt, nltk.Tree) ]
    # print(named_entities_str)