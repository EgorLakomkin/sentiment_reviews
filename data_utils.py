#-*-coding:utf-8-*-
import os, sys

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join( CURRENT_DIR, "data" )


class REVIEW_MARK:
    POSITIVE = 1
    NEGATIVE = 2
    NO_INFO = 0

class Review:

    def __init__(self, text, review_class = REVIEW_MARK.NO_INFO):
        self.text = text
        self.review_class = review_class


    def __repr__(self):
        return self.text



def load_booking_reviews():
    """


    :return:
    """
    import xml.etree.cElementTree as ET

    BOOKING_XML_FILE = os.path.join( DATA_DIR, "booking.xml" )
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse( BOOKING_XML_FILE, parser = parser )
    root = tree.getroot()

    reviews = []
    for item in root:
        for child in item:
            if child.tag == "Positivereview":
                review_text = child.text
                if review_text is not None:
                    if not isinstance( review_text, unicode ):
                        review_text = review_text.decode('utf-8')
                    reviews.append( Review( review_text, REVIEW_MARK.POSITIVE ) )
            if child.tag == "Negativereview":
                review_text = child.text
                if review_text is not None:
                    if not isinstance( review_text, unicode ):
                        review_text = review_text.decode('utf-8')
                    reviews.append( Review( review_text, REVIEW_MARK.NEGATIVE ) )
    return reviews


if __name__ == "__main__":
    reviews = load_booking_reviews()
    print "Loaded {} reviews".format( len(reviews) )