from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = "This is an example of showing stop word filtration."
stop_words = set(stopwords.words("english"))
print(stop_words)

words = word_tokenize(text)

filtered_sent = []

for w in words:
    if w not in stop_words:
        filtered_sent.append(w)
print(filtered_sent)

# probably won't use this