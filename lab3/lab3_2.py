import nltk
from nltk.corpus import names
import random
from nltk.classify import apply_features
import numpy


# nltk.download('names')

# 1.1 gender identification
# https://www.nltk.org/book/ch06.html

def gender_features(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    features["last_two_letters"] = name[:-2].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features


def get_labeled_names():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                     [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(labeled_names)
    return labeled_names


def get_accuracy():
    labeled_names = get_labeled_names()
    train_set = apply_features(gender_features, labeled_names[500:])
    test_set = apply_features(gender_features, labeled_names[:500])

    print("Training data...")
    print("Desicion Tre...")
    classifier_dec_tree = nltk.DecisionTreeClassifier.train(train_set)
    print("Naive Bayes...")
    classifier_naive_b = nltk.NaiveBayesClassifier.train(train_set)
    print("Maximum Entropy....")
    classifier_max_e = nltk.MaxentClassifier.train(train_set, max_iter=10)

    print("\nDecision Tree Accuracy: ", nltk.classify.accuracy(classifier_dec_tree, test_set))
    print("\nNaive Bayes Accuracy: ", nltk.classify.accuracy(classifier_naive_b, test_set))
    print("\nMaximum Emtropy Accuracy: ", nltk.classify.accuracy(classifier_max_e, test_set))


if __name__ == "__main__":
    get_accuracy()
