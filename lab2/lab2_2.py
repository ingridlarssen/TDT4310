import nltk
from nltk.corpus import brown
from nltk.corpus import nps_chat
from nltk.tag import DefaultTagger
from nltk import UnigramTagger
from nltk.tag import RegexpTagger
from nltk import FreqDist, BigramTagger

brown_corpus = [sent for sent in brown.tagged_sents()]
brown_spl_90 = int(90*len(brown_corpus)/100)
brown_spl_50 = int(50*len(brown_corpus)/100)

nps_chat_corpus = [sent for sent in nps_chat.tagged_posts()]
nps_spl_90 = int(90*len(nps_chat_corpus)/100)
nps_spl_50 = int(50*len(nps_chat_corpus)/100)

#train and test with 50/50
train_brown_50 = brown_corpus[:brown_spl_50]
test_brown_50 = brown_corpus[brown_spl_50:]
train_nps_50 = nps_chat_corpus[:nps_spl_50]
test_nps_50 = nps_chat_corpus[nps_spl_50:]

#train and test with 90/10
train_brown_90 = brown_corpus[:brown_spl_90]
test_brown_10 = brown_corpus[brown_spl_90:]
train_nps_90 = nps_chat_corpus[:nps_spl_90]
test_nps_10 = nps_chat_corpus[nps_spl_90:]

def find_accuracy(train_set, test_set):
    #skal alt her være test-set?
    train_words = [word for sent in train_set for word in sent]
    train_set_tags = [tag for (word, tag) in train_words]
    train_set_most_frequent_tag = FreqDist(train_set_tags).max()
    default_tagger = DefaultTagger(train_set_most_frequent_tag)
    accuracy_result = default_tagger.evaluate(test_set)
    return accuracy_result


#2a tag using defaulttagger and print accuracy of each testing set
def default_tagger_accuracy():
    print("DEFAULT TAGGER ACCURACY:")

    test_brown_result_50 = find_accuracy(train_brown_50, test_brown_50)
    print("Test Data Accuracy, Brown, 50% split: ", test_brown_result_50)

    test_brown_result_10 = find_accuracy(train_brown_90, test_brown_10)
    print("Test Data Accuracy, Brown, 10% split: ", test_brown_result_10)

    test_nps_result_50 = find_accuracy(train_nps_50, test_nps_50)
    print("Test Data Accuracy, NPS Chat, 50% split: ", test_nps_result_50)

    test_nps_result_10 = find_accuracy(train_nps_90, test_nps_10)
    print("Test Data Accuracy, NPS Chat, 10% split: ", test_nps_result_10)

#2b
def combined_taggers_accuracy():
    print("\nCombined Taggers Accuracy: ")

    #finding most used tag
    train_words = [word for sent in train_brown_50 for word in sent]
    train_set_tags = [tag for (word, tag) in train_words]
    most_frequent_tag = FreqDist(train_set_tags).max()
    default_tagger = DefaultTagger(most_frequent_tag)

    #default tagger
    default_tagger_result = default_tagger.evaluate(test_brown_50)
    print("Default Tagger accuracy: ", default_tagger_result)

    # regex tagger
    patterns = [
        (r'.*ing$', 'VBG'),  # gerunds
        (r'.*ed$', 'VBD'),  # simple past
        (r'.*es$', 'VBZ'),  # 3rd singular present
        (r'.*ould$', 'MD'),  # modals
        (r'.*\'s$', 'NN$'),  # possessive nouns
        (r'.*s$', 'NNS'),  # plural nouns
        (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # cardinal numbers
        (r'.*', 'NN')  # nouns (default)
    ]
    regex_tagger = RegexpTagger(patterns)
    regex_tagger_result = regex_tagger.evaluate(test_brown_50)
    print("\nRegex Tagger Accuracy: ", regex_tagger_result)

    #unigram tagger with default tagger as backoff
    unigram_tagger = UnigramTagger(train_brown_50, backoff=default_tagger)
    unigram_tagger_result = unigram_tagger.evaluate(test_brown_50)
    print("\nUnigram Tagger accuracy (Backoff = Default Tagger): ", unigram_tagger_result)

    # bigram tagger with different backoffs
    bigram_tagger = BigramTagger(train_brown_50)
    bigram_tagger_backoff_unigram = BigramTagger(train_brown_50, backoff=unigram_tagger)
    bigram_tagger_backoff_regex = BigramTagger(train_brown_50, backoff=regex_tagger)

    bigram_tagger_result = bigram_tagger.evaluate(test_brown_50)
    bigram_tagger_backoff_regex_result = bigram_tagger_backoff_regex.evaluate(test_brown_50)
    bigram_tagger_backoff_unigram_result = bigram_tagger_backoff_unigram.evaluate(test_brown_50)

    print("\nBigram Tagger Accuracy: ", bigram_tagger_result)
    print("Bigram Tagger Accuracy (Backoff = Regex Tagger): ", bigram_tagger_backoff_regex_result)
    print("Bigram Tagger Accuracy (Backoff = Unigram Tagger): ", bigram_tagger_backoff_unigram_result)


if __name__ == "__main__":
    #default_tagger_accuracy()
    combined_taggers_accuracy()


