from flask import Flask, jsonify
from flask import request
import spacy
from collections import defaultdict
from extract_nouns import yield_candidates
import joblib

from english_sentiment import empty_analyzer

app = Flask(__name__)
nlp = spacy.en.English(entity = False)

logreg_sentiment = joblib.load('./data/sentiment_logreg.pcl')

review_data = joblib.load("./data/topic_freqs.dat")
num_reviews = review_data[ "num_reviews" ]
topics_freq = review_data[ "topics_stats" ]

get_topic_proba = lambda x : (1.0 + topics_freq[x]) / ( 1.0 + num_reviews )

top_20_topics = set([
    'room', 'staff', 'location', 'bed', 'breakfast', 'hotel',
    'bathroom','service', 'view', 'food', 'shower', 'price',
    'bar', 'carpet', 'pillow', 'place', 'check', 'lobby'
])

def top_20_topic_filter( topic_struct ):
    return topic_struct["topic"].lower() in top_20_topics


def add_sentiments( topic_struct ):
    phrase = topic_struct['topic_phrase']
    prediction = logreg_sentiment.predict( [ phrase ] )[0]
    topic_struct['topic_sentiment'] = prediction

    return topic_struct


def merge_topic_info(lst_topic_info):
    """

    :param lst_topic_info:
    :return:
    """
    topic_info_dict = {}
    for info in lst_topic_info:
        topic_name = info["topic"]
        if topic_name not in topic_info_dict:
            topic_info_dict[ topic_name ] = {
                "topic_aspects" : []
            }
        topic_info_dict[ topic_name ][ "topic_aspects" ].append( info )
    return topic_info_dict

def add_topic_proba(topic_info):
    topic_name = topic_info["topic"]
    topic_proba = get_topic_proba( topic_name )
    topic_info["topic_proba"] = topic_proba
    return topic_info

@app.route('/extract_topics/<review>')
def extract_topic(review):
    if len(review) == 0:
        return jsonify({"status":"ERROR", "message" : "Review text should be non empty"})

    topics = list(yield_candidates( nlp, review ))
    #topics = filter( top_20_topic_filter, topics )
    topics = map( add_topic_proba, topics )
    topics = map(add_sentiments, topics)
    topic_merged_info = merge_topic_info( topics )
    return jsonify({"topics":topic_merged_info, 'review' :review })


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    app.run(host = '0.0.0.0',
            port = port, debug = False, use_reloader=False)

