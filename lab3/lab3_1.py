from nltk.corpus import wordnet as wn
import nltk
from nltk.corpus import movie_reviews as mr
import random

#!!use 64 bit to not get MemoryError in document_features

def get_mr_docs():
    documents = [(list(mr.words(fileid)), category) for category in mr.categories() for fileid in mr.fileids(category)]
    random.shuffle(documents)
    return documents

def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
        for synset in wn.synsets(word):
            for lemma in synset.lemma_names():
                features['synset({})'.format(lemma)] = (lemma in document_words)
    return features

def nb_classifier(documents, word_features):
    print("Finding feature sets..")
    featuresets = [(document_features(d, word_features), c) for (d, c) in documents]

    print("Defining train and test sets...")
    train_set, test_set = featuresets[100:], featuresets[:100]

    print("Training model...")
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("Accuracy: ", nltk.classify.accuracy(classifier, test_set))

if __name__ == "__main__":
    print("Retrieving documents...")
    mr_documents = get_mr_docs()
    all_words = nltk.FreqDist(w.lower() for w in mr.words())
    word_features = list(all_words)[:2000]
    nb_classifier(mr_documents, word_features)




