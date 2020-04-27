import nltk
from nltk.corpus import brown

GRAMMAR = """
	NP: {<DT>?<JJ.*>*<NN.>+}
	INFO: {<VB.><IN><NP>}
	"""


def find_sorted_sents(sents, nr=20):
    result = []

    cp = nltk.RegexpParser(GRAMMAR)
    for s in sents:
        tree = cp.parse(s)
        for st in tree.subtrees():
            if st.label() == "INFO":
                result.append(st)

    result_sorted = sorted(result, key=lambda x: x[0][0].lower())[:nr]
    return result_sorted


if __name__ == "__main__":
    sents = brown.tagged_sents()
    sorted_sents = find_sorted_sents(sents)
    print("Result (sorted): ")
    for sent in sorted_sents:
        print(sent)
