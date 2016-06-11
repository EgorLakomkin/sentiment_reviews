from data_utils import load_booking_reviews
import spacy


if __name__ == "__main__":
    reviews = load_booking_reviews()
    nlp = spacy.en.English()
    for review in reviews:
        review_text = review.text

        doc = nlp( review_text, entity = False )

        for np in doc.noun_chunks:
            print np.text