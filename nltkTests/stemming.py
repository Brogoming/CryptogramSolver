from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
example_words = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]

# for w in example_words:
#     print(ps.stem(w))

text = "It is very important to be pythonly while you are pythoning with python. All pythoners have pythoned at least once."
words = word_tokenize(text)

for w in words:
    print(ps.stem(w))

# probably won't use this