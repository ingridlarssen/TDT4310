'''Write a program to find all words that occur at least k times
 in the first n words inBrownCorpus. k and n are input parameters of the function.'''
import nltk
nltk.download('brown')
from nltk.corpus import brown
from collections import Counter

def find_nr_of_words(n,k):
    tokens_brown = brown.words()
    brown_tokens_lower = [word.lower() for word in tokens_brown[0:n]]

    if n < 0 or k < 0 or k > len(brown_tokens_lower):
        print("unvalid value of n or k")
        return

    word_counter = Counter()

    for word in brown_tokens_lower:
        word_counter[word] += 1

    words_with_k_frequency = [(word,count) for word,count in word_counter.items() if count >= k]
    print(words_with_k_frequency)

if __name__ == '__main__':
    find_nr_of_words(150,4)