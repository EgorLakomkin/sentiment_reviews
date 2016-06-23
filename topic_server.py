from flask import Flask, jsonify
from flask import request
import spacy

from extract_nouns import yield_candidates

app = Flask(__name__)
nlp = spacy.en.English()

top_20_topics = set([
    'room', 'staff', 'location', 'bed', 'breakfast', 'hotel',
    'bathroom','service', 'view', 'food', 'shower', 'price',
    'bar', 'carpet', 'pillow', 'place', 'check', 'lobby'
])

def top_20_topic_filter( topic_struct ):
    return topic_struct["topic"] in top_20_topics

@app.route('/')
def extract_topic():
    review = u"The staff was bad."
    if len(review) == 0:
        return jsonify({"status":"ERROR", "message" : "Review text should be non empty"})
    topics = list(yield_candidates( nlp, review ))
    topics = filter( top_20_topic_filter, topics )

    return jsonify({"topics":topics})

if __name__ == '__main__':
    app.run(host = '0.0.0.0',
            port = 5000, debug = True, use_reloader=False)

