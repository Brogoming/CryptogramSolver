from nltk.corpus import brown as words
from nltk import FreqDist
import re

englishVocab = set(word.lower() for word in words.words() if re.search("^(?=[a-z']*$)(?=[^aeiou']*[aeiou])(?=[^bcdfghjklmnpqrstvwxyz']*[bcdfghjklmnpqrstvwxyz])[a-z']+$",word))
englishVocab.add('a')
englishVocab.add('i')
englishVocab = sorted(englishVocab, key=len)

print("Words: ",len(englishVocab))
