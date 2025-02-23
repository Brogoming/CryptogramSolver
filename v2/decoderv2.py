import string
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from nltk import FreqDist
from nltk.corpus import brown as words
from nltk.tokenize import word_tokenize

englishVocab = list(word.upper() for word in words.words())
englishVocab = sorted(englishVocab, key=len)

freqWordDist = FreqDist(words.words())
freqWordDist = [word[0].upper() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True) if word.isalpha()]

symbolMatch = {}

def symbolMatchingInit(inputMessage):
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            symbolMatch[symbol] = ""

def generate_cipher():
    alphabet = list(string.ascii_lowercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def encode_text(text, cipher):
    return ''.join(cipher.get(c, c) for c in text.lower())

def createFeatureList(text, index):
    # print("createFeatureList")
    features = []

    # 1. Letter Frequencies (normalized count)
    letterFreqs = FreqDist(text)
    letterTotal = sum(letterFreqs.values())
    letterFreqsNormalized = {letter: count / letterTotal for letter, count in letterFreqs.items()}
    letter = text[index].lower()
    letterFreq = letterFreqsNormalized.get(letter, 0)  # Get normalized frequency for this letter
    features.append(letterFreq)

    # 2. Bigram Frequencies
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigramFreqs = FreqDist(bigrams)
    bigram = text[index - 1:index + 1] if index > 0 else ""
    bigramFreq = bigramFreqs.get(bigram, 0) / len(bigrams) if len(bigrams) > 0 else 0  # Normalize bigram frequency
    features.append(bigramFreq)

    # 3. Trigram Frequencies
    trigrams = [text[i:i + 3] for i in range(len(text) - 2)]
    trigramFreqs = FreqDist(trigrams)
    trigram = text[index - 2:index + 2] if index > 0 else ""
    trigramFreq = trigramFreqs.get(trigram, 0) / len(trigrams) if len(
        trigrams) > 0 else 0  # Normalize trigram frequency
    features.append(trigramFreq)

    # 4. Word Shape (e.g., _e__o for "hello")
    wordStart = text.rfind(' ', 0, index) + 1
    wordEnd = text.find(' ', index) if text.find(' ', index) != -1 else len(text)
    word = text[wordStart:wordEnd]
    wordShape = ''.join('_' if c.isalpha() else c for c in word)

    # Use number of underscores as the feature for word shape
    wordShapeUnderscoreCount = wordShape.count('_')
    features.append(wordShapeUnderscoreCount)

    # 5. Letter Position (First, Middle, Last)
    wordPosition = 1  # Default to middle
    if index == wordStart:  # First letter of the word
        wordPosition = 0
    elif index == wordEnd - 1:  # Last letter of the word
        wordPosition = 2
    features.append(wordPosition)

    # 5. Common Words Check
    word = ''.join(c for c in text[wordStart:wordEnd] if c.isalpha()).lower()
    isCommonWord = 1 if word in freqWordDist else 0
    features.append(isCommonWord)

    # Return the feature vector
    return features

def processMessage(ciphertext, model):
    decrypted = []
    used_letters = set()  # Set to track used letters in the decryption
    letter_mapping = {}  # Dictionary to store current letter mappings
    letter_freq = {}  # Dictionary to track frequency of letters (for prioritization)

    # Count letter frequencies from the encrypted message to help prioritize
    for letter in ciphertext:
        if letter.isalpha():
            letter_freq[letter] = letter_freq.get(letter, 0) + 1

    for i, letter in enumerate(ciphertext):
        if letter.isalpha():  # Only predict for alphabetic characters
            features = createFeatureList(ciphertext, i)
            prediction = model.predict([features])[0]

            # If the predicted letter is already assigned, try a different one
            while prediction in used_letters and letter not in letter_mapping.keys():
                # Try to prioritize less used letters in the encrypted message
                available_letters = [c for c in string.ascii_lowercase if c not in used_letters]

                if available_letters:
                    # Prioritize letters based on frequency
                    available_letters = sorted(available_letters, key=lambda x: letter_freq.get(x, 0), reverse=True)
                    prediction = available_letters[0]  # Pick the most frequent remaining letter
                else:
                    print(f"Warning: No available letters for position {i}. Decryption may be incomplete.")
                    prediction = '?'  # Use a placeholder or fallback letter
                    break
            if letter not in letter_mapping.keys():
                # Add the predicted letter to the used letters set
                used_letters.add(prediction)

                # Map the letter and add to the decrypted message
                letter_mapping[ciphertext[i]] = prediction
                decrypted.append(prediction)
            else:
                decrypted.append(letter_mapping[letter])
        else:
            decrypted.append(letter)  # Keep non-alphabetic characters intact

    # Show the letter mapping for clarity
    print("Letter Mapping:", letter_mapping)

    return ''.join(decrypted)
    # decrypted = []
    # letterFreq = {}
    # tokens = word_tokenize(ciphertext)
    #
    # # Count letter frequencies from the encrypted message to help prioritize
    # for symbol in ciphertext:
    #     if symbol.isalpha():
    #         letterFreq[symbol] = letterFreq.get(symbol, 0) + 1
    #
    # for token in tokens:
    #     decryptedWord = []
    #     for i, symbol in enumerate(token):
    #         if symbolMatch[symbol] == "":
    #             features = createFeatureList(token, i)
    #             prediction = model.predict([features])[0]
    #
    #             while prediction in symbolMatch.values():
    #                 availableLetters = [c for c in string.ascii_lowercase if c not in symbolMatch.values()]
    #
    #                 if availableLetters:
    #                     # Prioritize letters based on frequency
    #                     availableLetters = sorted(availableLetters, key=lambda x: letterFreq.get(x, 0), reverse=True)
    #                     prediction = availableLetters[0]  # Pick the most frequent remaining letter
    #                 else:
    #                     print(f"Warning: No available letters for position {i}. Decryption may be incomplete.")
    #                     prediction = '?'  # Use a placeholder or fallback letter
    #                     break
    #             symbolMatch[symbol] = prediction
    #             decryptedWord.append(prediction)
    #         else:
    #             decryptedWord.append(symbolMatch[symbol])
    #     decrypted.append(''.join(decryptedWord))
    # print(symbolMatch)
    # return ' '.join(decrypted)

def trainModel():
    print("Training...")
    X_train = []
    y_train = []

    # Create training data using random ciphers
    plaintext = "the quick brown fox jumps over the lazy dog"

    for _ in range(1000):  # Generate multiple samples
        cipher = generate_cipher()
        encoded = encode_text(plaintext, cipher)

        # For each letter in the ciphertext, treat it as a sample
        for i, letter in enumerate(encoded):
            if letter.isalpha():  # Only use letters as valid data points
                X_train.append(createFeatureList(encoded, i))
                y_train.append(plaintext[i])  # Corresponding plaintext letter

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print("Training Complete")
    return clf

if __name__=="__main__":
    # Train the model
    clf = trainModel()

    # Example encrypted message
    encryptedMessage = "iwd xtezl hcksr uky qtvfp kgdc iwd abom jkn" # "the quick brown fox jumps over the lazy dog"
    symbolMatchingInit(encryptedMessage)
    decryptedMessage = processMessage(encryptedMessage, clf)
    print("Decrypted message:", decryptedMessage)
