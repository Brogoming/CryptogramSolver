from nltk.tokenize import sent_tokenize, word_tokenize

example_text = "A BACD EFHG. A IJAKC LFM you'll, you should shower"

print(sent_tokenize(example_text))
print(word_tokenize(example_text))

# probably use this