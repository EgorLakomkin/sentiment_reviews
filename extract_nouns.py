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
    print root.dep_, root
    if root.dep_ != "nsubj":
        return False

    return True

def get_candidate_sentiment_phrases( doc, noun_phrase ):
    root = noun_phrase.root
    res = []
    for node in  root.head.subtree:
        if node_acomp_filter( node ):
            res.append( (list(root.head.subtree), noun_phrase,  node) )

    return res


def yield_candidates( nlp_obj, text ):

    doc = nlp_obj( text, entity = False )
    doc[:].root.dep = 410
    for np in doc.noun_chunks:
        if filter_noun_phrase( np, doc ):
            acomp_nodes = get_candidate_sentiment_phrases(  doc, np )
            if len(acomp_nodes) > 0:
                for phrase, np, acomp_node in acomp_nodes:
                    res = {}
                    res['topic'] =  np.root.lemma_.lower()
                    res['topic_acomp'] = acomp_node.lemma_.lower()
                    res['topic_phrase'] = [unicode(n)  for n in phrase]
                    res["topic_sentiment"] = 0.5
                    yield res

if __name__ == "__main__":
    reviews = load_booking_reviews()
    nlp = spacy.en.English()

    freq_stats = defaultdict( float )

    topic_stats = defaultdict(list)

    for review in reviews:

        review_text = review.text

        for res in yield_candidates( nlp, review_text ):

            print res['topic'], "->", res['topic_acomp']
            print res['topic_phrase']
            topic_stats[ res['topic'] ].append( res['topic_acomp']  )


    print "Total nodes", len(topic_stats)
    topic_freq = {n: len(s) for n, s in topic_stats.iteritems() }
    sorted_by_freq = sorted( topic_freq.iteritems(), key = lambda x: x[1], reverse= True )
    for t, freq in sorted_by_freq[:20]:
        print t, freq
    num_docs = len(reviews)
