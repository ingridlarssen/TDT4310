'''ex 1'''
from collections import Counter
import nltk
from nltk.corpus import brown

def most_frequent_tag():
    text = brown.tagged_words()
    pos_counts = nltk.FreqDist(tag for (word, tag) in text)
    print("the most common tag is ", pos_counts.most_common(1))


def ambiguous_words():
    text = brown.tagged_words()
    data = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in text)
    ambiguous_words = []

    for word in data.conditions():
        if len(data[word]) > 3:
            tags = data[word].keys()
            ambiguous_words.append((word, ' '.join(tags)))

    return ambiguous_words

#words that appear with at least two different tags
def nr_of_ambiguous_words():
    return len(ambiguous_words())


def percentage_ambiguous_words():
    len_ambiguous_words = nr_of_ambiguous_words()
    all_words = len(brown.tagged_words())
    return len_ambiguous_words/all_words*100


#Find top 10 words with the greatest number of distinct tags.  Print these words with their tags
def most_ambiguous_words(count=10):
    words = ambiguous_words()
    counter = Counter()

    for word, tags in words:
        counter[word, tags] = len(tags.split())

    return counter.most_common(count)

def find_sentences_with_most_ambiguous_words():
    amb_word = most_ambiguous_words(1)[0][0][0]
    tags = most_ambiguous_words(1)[0][0][1]
    sentences = brown.tagged_sents()

    sents_with_word = []
    not_added_tags = tags.split()

    for sentence in sentences:
        for word, tag in sentence:
            if word.lower() == amb_word and tag in not_added_tags:
                sents_with_word.append(sentence)
                not_added_tags.remove(tag)

    #from list with word,tag pairs to list with sentences (strings)
    prettier_sents_with_word = []
    for sentence in sents_with_word:
        sent = ""
        for word, tag in sentence:
            sent += word + " "
        prettier_sents_with_word.append([sent])

    return prettier_sents_with_word


if __name__ == "__main__":
    #most_frequent_tag()
    #print(nr_of_ambiguous_words())
    #print(percentage_ambiguous_words())
    #print(ambiguous_words())
    #print(most_ambiguous_words())
    print(find_sentences_with_most_ambiguous_words())
