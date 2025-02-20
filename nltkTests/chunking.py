import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

trainText = state_union.raw("2005-GWBush.txt")
sampleText = state_union.raw("2006-GWBush.txt")

customSentTokenizer = PunktSentenceTokenizer(trainText)

tokenized = customSentTokenizer.tokenize(sampleText)

def processContent():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)

            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}""" # we're looking for parts of speach with an adverb > verb > proper noun > noun

            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)

            chunked.draw()
    except Exception as e:
        print(str(e))

processContent()

# probably won't use