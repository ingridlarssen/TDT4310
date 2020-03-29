import nltk
from nltk.book import text9

'''2a) find complete sentence that contains the word at index  text9.index('sunset')'''
def find_complete_sentence(index):
    i = index
    '''+i to get correct index in original text9, since the slice methods creates new list, i - x to take a new list that is traversed backwards'''
    splice_end = text9[i:-1].index('.') + i
    splice_start = i - text9[(i-1):0:-1].index('.')

    return text9[splice_start:splice_end]


'''2b) Write program that returns all sentences with specific word'''
def find_all_sentences(input_word):
    sents = []
    i = 0
    for word in text9:
        if word == input_word: sents.append(find_complete_sentence(i))
        i = i + 1

    return sents

