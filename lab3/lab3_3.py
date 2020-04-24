from collections import defaultdict

'''
The base model
'''


class Model(object):
    def __init__(self):
        self.counts = defaultdict(float)
        self.counts['total'] = 0.0
        self.wordcounts = defaultdict(float)
        self.wordcounts['total'] = 0.0
        self.words = defaultdict(float)
        self.allwords = defaultdict(float)

    def train(self, type, examples):
        if not type in self.counts:
            self.counts[type] = 0.0
        if not type in self.wordcounts:
            self.wordcounts[type] = 0.0
        for example in examples:
            self.counts['total'] += 1.0
            self.counts[type] += 1.0
            if not type in self.words:
                self.words[type] = defaultdict(float)
            for word in example.split(' '):
                self.wordcounts['total'] += 1.0
                self.wordcounts[type] += 1.0
                self.allwords[word] = True
                if not word in self.words[type]:
                    self.words[type][word] = 1.0
                else:
                    self.words[type][word] += 1.0

    def prior(self, type):
        return self.implementation.prior(type)

    def probability(self, word, type):
        return self.implementation.probability(word, type)

    def classify(self, type, data):
        return self.implementation.classify(type, data)


'''
Model with smoothing option
'''


class Smoothing(Model):
    def __init__(self, k=1):
        Model.__init__(self)
        self.k = k

    def prior(self, type):
        return (self.counts[type] + self.k) / (self.counts['total'] + (self.k * len(self.words.keys())))

    def probability(self, word, type):
        a = self.words[type][word] + self.k
        b = self.wordcounts[type] + (self.k * len(self.allwords))
        return a / b

    def classify(self, type, data):
        if not isinstance(data, list):
            a = self.probability(data, type) * self.prior(type)
            b = 0.0
            for _type in self.words:
                b += self.probability(data, _type) * self.prior(_type)
            return a / b
        else:
            a = self.prior(type)
            for word in data:
                a *= self.probability(word, type)
            b = 0.0
            for _type in self.words:
                bb = self.prior(_type)
                for word in data:
                    bb *= self.probability(word, _type)
                b += bb
            return a / b


class MaximumLikelihood(Smoothing):
    def __init__(self, k=0):
        Smoothing.__init__(self, k)


#####################################################################################################################################
# Read me: The classifier model:																												#
#	funtions:																														#
#	1- initialization(k) of the model																								#
#       - k == 0: no-smooth mode 																									#
#       - k != 0: smooth mode																										#
#	2- prior(label) : get prior probability of label in the model																	#
#	3- probability(feature, label) :  the probability that input values with that label will have that feature						#
#	4- classify(label, data) :  the probability that input data is classified as label						 						#
#####################################################################################################################################

def Lab3_3a():
    print('Lab3_3a')
    MOVIE = ['a perfect world', 'my perfect woman', 'pretty woman']
    SONG = ['a perfect day', 'electric storm', 'another rainy day']

    model = MaximumLikelihood(1)
    model.train('movie', MOVIE)
    model.train('song', SONG)


    """
        YOUR CODE HERE!

        Returns the values.
        1. Prior probability of labels used in training. (movie, song)
        2. Probability of word under given prior label (i.e., P(word|label)) according to this model.
                a. P(perfect|movie)
                b. P(storm|movie)
                c. P(perfect|song)
                d. P(storm|song)
        3. Probability of the title 'perfect storm' is labeled as 'movie' and 'song' with no-smooth mode and smooth mode (k=1)
    """
    print("___________________________________________________________")
    print("Lab3_3a_1: Prior probability of labels used in training\n")
    prior_prob_movie = model.prior('movie')
    prior_prob_song = model.prior('song')
    print("Prior probability for movie: ", prior_prob_movie)
    print("Prior probability for song: ", prior_prob_song)

    print("____________________________________________________________")
    print("\nLab3_3a_2 Probability of word under given prior label")
    print("P(prefect|movie): ", model.probability("perfect", "movie"))
    print("P(storm | movie): ", model.probability("storm", "movie"))
    print("P(perfect | song): ", model.probability("perfect", "song"))
    print("P(storm | song): ", model.probability("storm", "song"))

    print("____________________________________________________________")
    print("\nLab3_3a_3 Probability of the title 'perfect storm' is labeled movie and song")
    print("No smooth (k=0): \n")
    model2 = MaximumLikelihood(0)
    model2.train('movie', MOVIE)
    model2.train('song', SONG)
    print("P('movie'|'perfect storm') = ", model2.classify('movie', ['perfect', 'storm']))
    print("P('song'|'perfect storm') = ", model2.classify('song', ['perfect', 'storm']))

    print("Smooth (k=1): \n")
    print("P('movie'|'perfect storm') = ", model.classify('movie', ['perfect', 'storm']))
    print("P('song'|'perfect storm') = ", model.classify('song', ['perfect', 'storm']))


def Lab3_3b():
    print('\nLab3_3b')

    HAM = ["play sport today", "went play sport", "secret sport event", "sport is today", "sport costs money"]
    SPAM = ["offer is secret", "click secret link", "secret sport link"]

    model = MaximumLikelihood()
    model.train('S', SPAM)
    model.train('H', HAM)

    """
        YOUR CODE HERE!

        Returns the values.
        1. Prior probability of labels for SPAM, HAM data.
        2. Probability of word 'secret', 'sport' under given prior label (SPAM, HAM)
        3. Probabilities of: The word 'today is secret' is labeled as SPAM, HAM with no-smooth mode and smooth mode (k=1)

    """
    print("____________________________________________________")
    print("Lab3_3_3b_1: prior probability of labels for SPAM and HAM")

    prior_prob_s = model.prior('S')
    prior_prob_h = model.prior('H')
    print("Prior probability for SPAM: ", prior_prob_s)
    print("Prior probability for HAM: ", prior_prob_h)

    print("_______________________________________________________")
    print("Lab3_3_3b_2: probability of word 'secret', 'sport' under given prior label SPAM and HAM")
    print("P(secret|S): ", model.probability("secret", "S"))
    print("P(sport |S): ", model.probability("sport", "S"))
    print("P(secret |H): ", model.probability("secret", "H"))
    print("P(sport |H): ", model.probability("sport", "H"))

    print("________________________________________________________")
    print("Lab3_3_3b_3: probabilities of the word 'today is secret' is labeled as SPAM, HAM with no smooth and smooth mode")
    print("No smooth (k=0): ")
    model3 = MaximumLikelihood(0)
    model3.train('S', SPAM)
    model3.train('H', HAM)
    print("P(s|'today is secret'): ", model3.classify('S', ["today", "is", "secret"]))
    print("P(h|'today is secret': ", model3.classify('H', ["today", "is", "secret"]))

    print("Smooth (k=1): ")
    model2 = MaximumLikelihood(1)
    model2.train('S', SPAM)
    model2.train('H', HAM)
    print("P(s|'today is secret'): ", model2.classify('S', ["today", "is", "secret"]))
    print("P(h|'today is secret': ", model2.classify('H', ["today", "is", "secret"]))


if __name__ == '__main__':
    Lab3_3a()
    Lab3_3b()
