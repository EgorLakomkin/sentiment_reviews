from flask import Flask, jsonify
from flask import request
import spacy
from collections import defaultdict
from extract_nouns import yield_candidates

app = Flask(__name__)
nlp = spacy.en.English(entity = False)

top_20_topics = set([
    'room', 'staff', 'location', 'bed', 'breakfast', 'hotel',
    'bathroom','service', 'view', 'food', 'shower', 'price',
    'bar', 'carpet', 'pillow', 'place', 'check', 'lobby'
])

def top_20_topic_filter( topic_struct ):
    return topic_struct["topic"].lower() in top_20_topics

def merge_topic_info(lst_topic_info):
    """

    :param lst_topic_info:
    :return:
    """
    topic_info_dict = defaultdict(list)
    for info in lst_topic_info:
        topic_info_dict[ info["topic"] ].append( info )
    return topic_info_dict

@app.route('/extract_topics/<review>')
def extract_topic(review):
    if len(review) == 0:
        return jsonify({"status":"ERROR", "message" : "Review text should be non empty"})

    topics = list(yield_candidates( nlp, review ))
    topics = filter( top_20_topic_filter, topics )

    topic_merged_info = merge_topic_info( topics )
    return jsonify({"topics":topic_merged_info})


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    app.run(host = '0.0.0.0',
            port = port, debug = False, use_reloader=False)

