import nltk
from nltk.corpus import brown
from nltk import UnigramTagger
from nltk.corpus import nps_chat
from nltk import FreqDist, ConditionalFreqDist

brown_corpus_sents = [sent for sent in brown.tagged_sents()]
brown_spl_90 = int(90*len(brown_corpus_sents)/100)
brown_spl_50 = int(50*len(brown_corpus_sents)/100)
nps_chat_corpus_posts = [sent for sent in nps_chat.tagged_posts()]
nps_spl_90 = int(90*len(nps_chat_corpus_posts)/100)
nps_spl_50 = int(50*len(nps_chat_corpus_posts)/100)

train_brown_50 = brown_corpus_sents[:brown_spl_50]
test_brown_50 = brown_corpus_sents[brown_spl_50:]
train_nps_50 = nps_chat_corpus_posts[:nps_spl_50]
test_nps_50 = nps_chat_corpus_posts[nps_spl_50:]
train_brown_90 = brown_corpus_sents[:brown_spl_90]
test_brown_10 = brown_corpus_sents[brown_spl_90:]
train_nps_90 = nps_chat_corpus_posts[:nps_spl_90]
test_nps_10 = nps_chat_corpus_posts[nps_spl_90:]

def get_lookup_tagger_accuracy(test_set, lookup_tagger_basis, corpus):
    words = [word for sent in lookup_tagger_basis for word in sent]
    fd = FreqDist(words)
    cfd = ConditionalFreqDist(corpus.tagged_words())
    most_freq_words = fd.most_common(200)
    likely_tags = dict((word[0], cfd[word[0]].max()) for (word, _) in most_freq_words)
    baseline_tagger = UnigramTagger(model=likely_tags)
    result = baseline_tagger.evaluate(test_set)
    return result

def lookup_tagger_accuracy():
    #3a
    print("Lookup Tagger Accuracy, Brown \n")
    print("Brown 50-50% split: ", get_lookup_tagger_accuracy(train_brown_50, test_brown_50, brown_corpus_sents, brown))
    print("Brown 90-10% split: ", get_lookup_tagger_accuracy(train_brown_90, test_brown_10, brown_corpus_sents, brown))
    print("NPS Chat 50-50% split: ", get_lookup_tagger_accuracy(train_nps_50, test_nps_50, brown_corpus_sents, brown))
    print("NPS Chat 90-10% split: ", get_lookup_tagger_accuracy(train_nps_90, test_nps_10, brown_corpus_sents, brown))

    #3b
    print("___________________________________________\nLookup Tagger Accuracy, NPS Chat \n")
    print("Brown 50-50% split: ", get_lookup_tagger_accuracy(train_brown_50, test_brown_50, nps_chat_corpus_posts, nps_chat))
    print("Brown 90-10% split: ", get_lookup_tagger_accuracy(train_brown_90, test_brown_10, nps_chat_corpus_posts, nps_chat))
    print("NPS Chat 50-50% split: ", get_lookup_tagger_accuracy(train_nps_50, test_nps_50, nps_chat_corpus_posts, nps_chat))
    print("NPS Chat 90-10% split: ", get_lookup_tagger_accuracy(train_nps_90, test_nps_10, nps_chat_corpus_posts, nps_chat))

if __name__ == "__main__":
    lookup_tagger_accuracy()