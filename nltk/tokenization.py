from nltk.tokenize import sent_tokenize, word_tokenize

example_text = "Hello Mr. Smith, how are you doing today? The whether is great and Python is awesome! The sky is blue."

print(sent_tokenize(example_text))
print(word_tokenize(example_text))

# probably use this