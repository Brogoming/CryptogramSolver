from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize

sampleText = gutenberg.raw('bible-kjv.txt')

tok = sent_tokenize(sampleText)
print(tok[5:15])