from nltk.util import ngrams
print(list(ngrams("chick", 3)))

# https://www.nltk.org/api/nltk.util.html#nltk.util.ngrams

import nltk
from nltk.lm import MLE  # Maximum Likelihood Estimation (basic model)
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize import word_tokenize

# Example training text (you can use a large corpus instead)
text = "This is a cryptogram solver. a cryptogram is a type of puzzle."

# Tokenize the text into words
tokens = [word_tokenize(text.lower())]  # Convert to lowercase for consistency

# Convert tokens into bigrams (2-grams)
n = 2  # Bigram model
train_data, vocab = padded_everygram_pipeline(n, tokens)

# Initialize and train the model
bigram_model = MLE(n)  # MLE is the basic N-gram model
bigram_model.fit(train_data, vocab)

# Generate text based on the model
print("Generated sentence:", " ".join(bigram_model.generate(5, text_seed=["this"])))

# Predict the probability of a word following another word
print("Probability of 'is' given 'this':", bigram_model.score("is", ["this"]))
print("Probability of 'a' given 'cryptogram':", bigram_model.score("a", ["cryptogram"]))
