from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score

from sentiment.load import load_sst
from  sentiment import Tree
from sklearn.pipeline import Pipeline
import joblib
from collections import Counter
import itertools


def getWords(tree):
    res = []
    for leaf_node in tree.leaf:
        res.append(leaf_node.word)
    return res

def empty_analyzer(x):
    return x

if __name__ == "__main__":
    _, X_trees_train, X_trees_dev, X_trees_test, _ = load_sst()

    print "Train trees: {}, dev trees: {}, test trees: {}".format( len(X_trees_train),
                                                                   len(X_trees_dev), len(X_trees_test) )


    first_train_tree = X_trees_train[ 0 ]

    print getWords( first_train_tree )

    train_sentences_generator = [getWords(tree)
                                 for tree in itertools.chain(X_trees_train, X_trees_dev, X_trees_test)   ]

    train_labels = [tree.get_whole_sentence_label()
                    for tree in itertools.chain(X_trees_train, X_trees_dev, X_trees_test) ]

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode',
                        analyzer= empty_analyzer, ngram_range=(1, 2), use_idf=1, smooth_idf=1,
                        sublinear_tf=1)),

        #('svd', TruncatedSVD(n_components = 30)),

        ('logreg', LogisticRegression(penalty='l2', dual=True, tol=0.0001,
                           C=1, fit_intercept=True, intercept_scaling=1.0,
                           class_weight=None, random_state=None))
    ])

    print "Fitting logistic regression"
    pipeline.fit( train_sentences_generator, train_labels )
    joblib.dump( pipeline, './data/sentiment_logreg.pcl' )
    print "Fitted"
    print Counter( train_labels )

    X_test = [ getWords(tree) for tree in X_trees_test ]
    Y_test = [ tree.get_whole_sentence_label() for tree in X_trees_test ]

    Y_pred = pipeline.predict( X_test )
    random_guess = [ 3 for tree in X_trees_test ]

    print confusion_matrix( Y_test, Y_pred )

    print "tf-idf + logreg", accuracy_score( Y_test, Y_pred )
    print "random guess", accuracy_score(Y_test, random_guess)

