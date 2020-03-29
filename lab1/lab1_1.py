# exercise 1, explanation task.
# 29/03/2020, Ingrid Larssen

# !/usr/bin/env python3

import nltk
from collections import Counter

MALE = 'male'
FEMALE = 'female'
UNKNOWN = 'unknown'
BOTH = 'both'

MALE_WORDS = set([
    'guy', 'spokesman', 'chairman', "men's", 'men', 'him', "he's", 'his',
    'boy', 'boyfriend', 'boyfriends', 'boys', 'brother', 'brothers', 'dad',
    'dads', 'dude', 'father', 'fathers', 'fiance', 'gentleman', 'gentlemen',
    'god', 'grandfather', 'grandpa', 'grandson', 'groom', 'he', 'himself',
    'husband', 'husbands', 'king', 'male', 'man', 'mr', 'nephew', 'nephews',
    'priest', 'prince', 'son', 'sons', 'uncle', 'uncles', 'waiter', 'widower',
    'widowers'
])

FEMALE_WORDS = set([
    'heroine', 'spokeswoman', 'chairwoman', "women's", 'actress', 'women',
    "she's", 'her', 'aunt', 'aunts', 'bride', 'daughter', 'daughters', 'female',
    'fiancee', 'girl', 'girlfriend', 'girlfriends', 'girls', 'goddess',
    'granddaughter', 'grandma', 'grandmother', 'herself', 'ladies', 'lady',
    'lady', 'mom', 'moms', 'mother', 'mothers', 'mrs', 'ms', 'niece', 'nieces',
    'priestess', 'princess', 'queens', 'she', 'sister', 'sisters', 'waitress',
    'widow', 'widows', 'wife', 'wives', 'woman'
])


def genderize(words):
    '''creates an intersection of words present in both the argument words and MALE_WORDS and FEMALE WORDS respectively.
    Variable holds the length of this intersection.'''
    mwlen = len(MALE_WORDS.intersection(words))
    fwlen = len(FEMALE_WORDS.intersection(words))

    # checks the length of these variables
    # if there are only male words, return MALE
    if mwlen > 0 and fwlen == 0:
        return MALE
    # if there are only female words, return FEMALE
    elif mwlen == 0 and fwlen > 0:
        return FEMALE
    # if there are both male and female words, return BOTH
    elif mwlen > 0 and fwlen > 0:
        return BOTH
    # edge case, if no gendered words etc, return UNKNOWN
    else:
        return UNKNOWN


def count_gender(sentences):
    # sents holds the total number of sentences for each gender present in the sentences
    sents = Counter()
    # words holds the total number of words in these sentences for each gender present in the sentences
    words = Counter()

    for sentence in sentences:
        gender = genderize(sentence)
        # counters increase based on the result from genderize on previous line
        sents[gender] += 1
        words[gender] += len(sentence)

    return sents, words


def parse_gender(text):

    '''the text (input argument) is first segmented into sentences (by using sent_tokenize()).
    these sentences are then iterated over. For each sentence, all the words are made into consisting only lower letters.
    To iterate over the words, sentences are prepared by using word_tokenize, which from each sentences creates a list of strings (words)'''
    sentences = [
        [word.lower() for word in nltk.word_tokenize(sentence)]
        for sentence in nltk.sent_tokenize(text)
    ]

    sents, words = count_gender(sentences)
    #total holds the sum of the counters in words.
    total = sum(words.values())

    #iterate over the gender counters in words
    for gender, count in words.items():
        #find % of total
        pcent = (count / total) * 100
        nsents = sents[gender]
        #print % of total for each gender
        print(
            "{:0.3f}% {} ({} sentences)".format(pcent, gender, nsents)
        )


if __name__ == '__main__':
    with open('sample.txt', 'r') as f:
        parse_gender(f.read())
