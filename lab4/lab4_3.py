import nltk


GRAMMAR = r"""
  NP: {<NNP>*}
      {<DT>?<JJ>?<NNS>}
      {<NN><NN>}
"""


f = open("SpaceX.txt", "r")
contents = f.read()
cp = nltk.RegexpParser(GRAMMAR)

sentences = nltk.tokenize.sent_tokenize(contents)
for sent in sentences:
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = nltk.pos_tag(tokens)
    result = cp.parse(tags)

    print("Lab4_3 a)")
    print(result)

    print("Lab4_3 b)")
    for st in result.subtrees():
        if st.label() == "NP":
            out = ""
            for leaf in st.leaves():
                out += leaf[0] + " "
            print(out)
