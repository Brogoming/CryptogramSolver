from nltk.probability import FreqDist
from nltk.corpus import words
english_vocab = set(words.words())
text = "".join(english_vocab).upper()
freq_dist = FreqDist(text)
print(freq_dist)