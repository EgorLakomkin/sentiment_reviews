from data_utils import load_booking_reviews
import spacy
from collections import defaultdict

np_root_filter_list = [ "i", "we", "it", "you", "they", "she", "he", "nothing"]

adj_filter_list = [ "my", "our", "other", "more", "your", "all", "first", "next", "that", "better",
                    "only", "mich", "its", "whole", "such", "second", "same", "most", "few", "overall",
                    "sure", "open", "last", "his", "due", "able", "non", "many", "much"]


def noun_chunk_to_head_noun(chunk):
    """Given a chunk, find the noun who's head is outside the chunk. This is the head noun"""
    nouns = [t for t in chunk if t.pos_ == "NOUN"]
    if len(nouns) == 0:
        raise Exception("0 noun in chunk")
    if len(nouns) > 1:
        raise Exception(">1 nouns in chunk")
    return nouns[0]

def node_acomp_filter(node):
    #if node.dep_ == "acomp":
    #    return True
    if node.lemma_ in adj_filter_list or node.lower_ in adj_filter_list:
        return False
    if node.pos_ == "ADJ":
        return True

    return False

def filter_noun_phrase(noun_phrase, doc):
    head_noun = noun_chunk_to_head_noun( noun_phrase )
    if head_noun is None:
        return False
    if head_noun.lemma_ in np_root_filter_list:
        return False
    print head_noun.dep_, head_noun
    if head_noun.dep_ not in ["nsubj", "root"]:
        print "filterint out", head_noun.lemma_, head_noun.dep_
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
    import joblib
    reviews = load_booking_reviews()
    nlp = spacy.en.English()

    freq_stats = defaultdict( float )

    topic_stats = defaultdict(list)
    adj_stats =  defaultdict(int)

    test = list( yield_candidates( nlp, u"good facilities and great staff" ) )

    for review in reviews:

        review_text = review.text

        print review_text
        for res in yield_candidates( nlp, review_text ):

            print res['topic'], "->", res['topic_acomp']
            print res['topic_phrase']
            topic_stats[ res['topic'] ].append( res['topic_acomp']  )
            adj_stats[ res['topic_acomp'] ] += 1
        print "====================="

    print "Total nodes", len(topic_stats)
    topic_freq = {n: len(s) for n, s in topic_stats.iteritems() }
    sorted_by_freq = sorted( topic_freq.iteritems(), key = lambda x: x[1], reverse= True )
    for t, freq in sorted_by_freq[:20]:
        print t, freq

    print "=========="
    for adj, adj_count in  sorted( adj_stats.iteritems(), key = lambda x: x[1], reverse= True ):
        print adj, "  ", adj_count
    num_docs = len(reviews)

    joblib.dump( { "topics_stats" : topic_freq, "num_reviews" : len(reviews)}, "./data/topic_freqs.dat" )