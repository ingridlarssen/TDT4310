import nltk
from nltk.corpus import brown
from nltk.corpus import nps_chat
from nltk.tag import DefaultTagger

brown_corpus = [word for word in brown.tagged_words()]
brown_spl_90 = int(90*len(brown_corpus)/100)
brown_spl_50 = int(50*len(brown_corpus)/100)

nps_chat_corpus = [word for word in nps_chat.tagged_words()]
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

def find_accuracy(test_set):
    test_set_tags = [tag for (word, tag) in test_set]
    test_set_most_frequent_tag = nltk.FreqDist(test_set_tags).max()
    default_tagger = DefaultTagger(test_set_most_frequent_tag)
    test_set_result = default_tagger.evaluate([test_set])
    return test_set_result


#2a tag using defaulttagger and print accuracy of each testing set
def test_set_default_tagger_accuracy():
    test_brown_result_50 = find_accuracy(test_brown_50)
    print("Test Data Accuracy, Brown, 50% split: ", test_brown_result_50)

    test_brown_result_10 = find_accuracy(test_brown_10)
    print("Test Data Accuracy, Brown, 10% split: ", test_brown_result_10)

    test_nps_result_50 = find_accuracy(test_nps_50)
    print("Test Data Accuracy, NPS Chat, 50% split: ", test_nps_result_50)

    test_nps_result_10 = find_accuracy(test_nps_10)
    print("Test Data Accuracy, NPS Chat, 10% split: ", test_nps_result_10)

#2b
def test_set_combined_taggers_accuracy():


if __name__ == "__main__":
    test_set_default_tagger_accuracy()


