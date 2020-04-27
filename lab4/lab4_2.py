import nltk
from nltk.tokenize import TweetTokenizer
import tweepy

consumer_key = "your key"
consumer_secret = "your key"
access_token = "your key"
access_token_secret = "your key"


def get_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def get_tweets(api, username, count=20):
    tweets = tweepy.Cursor(api.user_timeline, id=username, tweet_mode="extended").items(count)
    result = [tweet.full_text for tweet in tweets]
    return result


def get_ngram(tokens, N):
    ngrams = []
    for i in range(len(tokens) - N + 1):
        ngram = tokens[i:i + N]
        ngrams.append(ngram)
    return ngrams


def ngram_frequence(ngrams):
    counts = {}
    for ng in ngrams:
        seq = " ".join(ng[:-1])
        last = ng[-1]

        if seq not in counts:
            counts[seq] = {}
        if last not in counts[seq]:
            counts[seq][last] = 0

        counts[seq][last] += 1
    return counts


def gen_sentence(frequencies, text, N):
    last_N = " ".join(text.split()[-(N - 1):])
    if last_N not in frequencies:
        print("The word is not in the frequency distribution")
        return

    while not text.endswith(('.', '?', '!', ',')):
        best_choice = max(zip(frequencies[last_N].values(), frequencies[last_N].keys()))[1]
        text += " " + best_choice
        print(text)
        last_N = " ".join(text.split()[-(N - 1):])
    return text


def find_probability():
    print("probability")


if __name__ == '__main__':
    api = get_auth()
    username = 'realDonaldTrump'
    N = 3
    TEXT = "it is not"
    tweets = get_tweets(api, username, 3000)
    print("Fetched " + str(len(tweets)) + " tweets from " + username)
    ngrams = []
    tokenizer = TweetTokenizer()
    for tweet in tweets:
        ngrams += get_ngram(tokenizer.tokenize(tweet), N)
    frequencies = ngram_frequence(ngrams)
    print(gen_sentence(frequencies, TEXT, N))
