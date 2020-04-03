'''exersice 3: write program to build own custom corpus, print 10 most common words'''
import os
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import tweepy

consumer_key="your key"
consumer_secret="your key"
access_token="your key"
access_token_secret="your key"

def get_api_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_tweets_from_users(user_names,count=200):
    api = get_api_auth()

    for user_name in user_names:
        tweets = ""
        timeline = api.user_timeline(screen_name=user_name, count=count, tweet_mode="extended")

        for i in range(len(timeline)):
            #get full text from retweets.
            full_text_retweeted = timeline[i]._json.get("retweeted_status")

            if None != full_text_retweeted:
                tweets = tweets + " " + full_text_retweeted.get("full_text")
            else:
                tweets = tweets + " " + timeline[i]._json["full_text"]

        save_to_file(tweets, user_name, 'corpus/')


def save_to_file(text, file_name, folder):
    if folder and not os.path.isdir(folder):
        os.mkdir(folder)
    path = (folder or "") + file_name
    text_file = open(path + ".txt", "w", encoding="utf-8")
    text_file.write(text)
    text_file.close()


def tokenize_tweets_from_file(corpus_folder):
    text_string = ""
    for file_name in os.listdir(corpus_folder):
        with open(corpus_folder + file_name, encoding="utf8") as file:
            text_string = text_string + file.read()

    tweet_tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    tokens = tweet_tokenizer.tokenize(text_string)
    return tokens


#english stop words
def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    return [w for w in tokens if w not in stop_words]


def find_most_used_words(count=10):
    tokens = tokenize_tweets_from_file("corpus/")
    tokens_w_sw = remove_stop_words(tokens)

    fdist = FreqDist(tokens_w_sw)
    most_frequent_words = fdist.most_common(count)

    save_to_file(str(most_frequent_words), "result_ex_3", None)
    print(most_frequent_words)


def test_authentication():
    api = get_api_auth()
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")


if __name__ == "__main__":
    get_tweets_from_users(["realDonaldTrump", "AppleNews", "TheOfficialA7X", "YaleE360", "BernieSanders", "WHO", "Schwarzenegger", "KimKardashian", "Canada", "ArianaGrande"])
    find_most_used_words()