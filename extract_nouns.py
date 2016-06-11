from data_utils import load_booking_reviews
import spacy
from collections import defaultdict

filter_list = [ "i", "we", "it", "us", "you", "they", "she"]

if __name__ == "__main__":
    reviews = load_booking_reviews()
    nlp = spacy.en.English()

    freq_stats = defaultdict( float )

    for review in reviews:
        review_text = review.text

        doc = nlp( review_text, entity = False )

        for np in doc.noun_chunks:
            np_text = np.text.lower()
            if np_text not in filter_list:
                freq_stats[ np_text ] += 1

    num_docs = len(reviews)
