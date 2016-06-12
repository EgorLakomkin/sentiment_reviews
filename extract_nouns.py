from data_utils import load_booking_reviews
import spacy
from collections import defaultdict

np_root_filter_list = [ "i", "we", "it", "you", "they", "she", "he"]



def node_acomp_filter(node):
    if node.dep_ == "acomp":
        return True
    return False

def filter_noun_phrase(noun_phrase, doc):
    root = noun_phrase.root
    if root.lemma_ in np_root_filter_list:
        return False
    if root.dep_ != "nsubj":
        return False

    return True

def get_candidate_sentiment_phrases( doc, noun_phrase ):
    root = noun_phrase.root
    res = []
    for node in  root.head.subtree:
        if node_acomp_filter( node ):
            res.append( (list(root.head.subtree),np,  node) )

    return res

if __name__ == "__main__":
    reviews = load_booking_reviews()
    nlp = spacy.en.English()

    freq_stats = defaultdict( float )

    for review in reviews:
        review_text = review.text

        doc = nlp( review_text, entity = False )

        for np in doc.noun_chunks:

            if filter_noun_phrase( np, doc ):
                acomp_nodes = get_candidate_sentiment_phrases( doc, np )
                if len(acomp_nodes) > 0:
                    for phrase, np, acomp_node in acomp_nodes:
                        print np, "->", acomp_node
                        print phrase

    num_docs = len(reviews)
