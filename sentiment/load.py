
import os

current_dir = os.path.dirname(  os.path.realpath( __file__  ) )
DATA_DIR = os.path.join( current_dir, "..", "data" )
SST_DIR = os.path.join( DATA_DIR, "sentiment_treebank" )

import numpy as np
from Tree import Tree


def load_sst():
    print 'Load Trees...'
    with open(os.path.join(SST_DIR, 'STree.txt')) as f:
        trees = []
        for line in f.readlines():
            tree = line.split('|')
            tree = np.array(tree).astype(int)
            trees.append(tree)

    print 'Load Sentences...'
    with open(os.path.join(SST_DIR, 'SOStr.txt')) as f:
        sentences = []
        lexicon = set()
        for line in f.readlines():
            sent = line.strip().split('|')
            sentences.append(sent)
            lexicon = lexicon.union(sent)

    print 'Load data split'
    with open(os.path.join(SST_DIR, 'datasetSplit.txt')) as f:
        whichSet = []
        f.readline()
        for line in f.readlines():
            whichSet.append(int(line.strip().split(',')[1]))

    print 'Load Index...'
    with open(os.path.join(SST_DIR, 'dictionary.txt')) as f:
        index = {}
        for line in f.readlines():
            phrase = line.split('|')
            index[int(phrase[1])] = phrase[0]

    print 'Load Labels...'
    with open(os.path.join(SST_DIR, 'sentiment_labels.txt')) as f:
        f.readline()
        labels = {}
        for line in f.readlines():
            id_p, y = line.split('|')
            labels[index[int(id_p)]] = float(y)

    print 'Build Trees...'
    X_trees_train = []
    X_trees_dev = []
    X_trees_test = []
    for s, t, k in zip(sentences, trees, whichSet):
        if k == 1:
            X_trees_train.append(Tree(s, t, labels))
        elif k == 2:
            X_trees_test.append(Tree(s, t, labels))
        elif k == 3:
            X_trees_dev.append(Tree(s, t, labels))
        else:
            raise(Exception('Error parsing train/test/dev'))
    return lexicon, X_trees_train, X_trees_dev, X_trees_test, labels


if __name__ == "__main__":
    load_sst()