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

            namedEnt = nltk.ne_chunk(tagged)
            namedEnt.draw()

    except Exception as e:
        print(str(e))

processContent()
# maybe, I can see how it can be useful for sentence structure but not really for spelling

"""
NE Type and Examples
ORGANIZATION - Georgia-Pacific Corp., WHO
PERSON - Eddy Bonte, President Obama
LOCATION - Murray River, Mount Everest
DATE - June, 2008-06-29
TIME - two fifty a m, 1:30 p.m.
MONEY - 175 million Canadian Dollars, GBP 10.40
PERCENT - twenty pct, 18.75 %
FACILITY - Washington Monument, Stonehenge
GPE - South East Asia, Midlothian
"""