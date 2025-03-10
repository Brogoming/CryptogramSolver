import string
import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from nltk import FreqDist
from nltk.corpus import brown as words

englishVocab = list(word.lower() for word in words.words())
englishVocab = sorted(englishVocab, key=len)

freqWordDist = FreqDist(words.words())
freqWordDist = [word[0].lower() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True) if word.isalpha()]

symbolMatch = {}

def symbolMatchingInit(inputMessage):
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            symbolMatch[symbol] = ""

def generateCipher(inputMessage):
    encodedLetters = {}
    availableAlpha = list("abcdefghijklmnopqrstuvwxyz")
    output = []

    for letter in inputMessage:
        if letter.isalpha():
            if letter not in encodedLetters:
                random.shuffle(availableAlpha)  # Shuffle to improve randomness
                randomChar = next((ch for ch in availableAlpha if ch != letter), availableAlpha[0])
                encodedLetters[letter] = randomChar
                availableAlpha.remove(randomChar)  # Remove assigned letter
            output.append(encodedLetters[letter])
        else:
            output.append(letter)

    return "".join(output)

def createFeatureList(text, index):
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

    # 6. Common Words Check
    word = ''.join(c for c in text[wordStart:wordEnd] if c.isalpha()).lower()
    isCommonWord = 1 if word in freqWordDist else 0
    features.append(isCommonWord)

    # Return the feature vector
    return features

def processMessage(ciphertext, model):
    decrypted = []
    letterFreq = {}

    # Count letter frequencies from the encrypted message to help prioritize
    for symbol in ciphertext:
        if symbol.isalpha():
            letterFreq[symbol] = letterFreq.get(symbol, 0) + 1

    for i, symbol in enumerate(ciphertext):
        if symbol.isalpha():
            if symbolMatch[symbol] != '':
                decrypted.append(symbolMatch[symbol])
            else:
                features = createFeatureList(ciphertext, i)
                prediction = model.predict([features])[0]

                while prediction in symbolMatch.values():
                    availableLetters = [c for c in string.ascii_lowercase if c not in symbolMatch.values()]

                    if availableLetters:
                        # Prioritize letters based on frequency
                        availableLetters = sorted(availableLetters, key=lambda x: letterFreq.get(x, 0), reverse=True)
                        prediction = availableLetters[0]  # Pick the most frequent remaining letter
                    else:
                        print(f"Warning: No available letters for position {i}. Decryption may be incomplete.")
                        prediction = '?'  # Use a placeholder or fallback letter
                        break
                symbolMatch[symbol] = prediction
                decrypted.append(symbolMatch[symbol])
        else:
            decrypted.append(symbol)
    return ''.join(decrypted)

def trainModel():
    print("Training...")
    X_train = []
    y_train = []

    # Create training data using random ciphers
    plaintext = "the quick brown fox jumps over the lazy dog"

    for _ in range(1000):  # Generate multiple samples
        encoded = generateCipher(plaintext)

        # For each letter in the ciphertext, treat it as a sample
        for i, letter in enumerate(plaintext):
            if letter.isalpha():  # Only use letters as valid data points
                X_train.append(createFeatureList(plaintext, i))
                y_train.append(plaintext[i])  # Corresponding plaintext letter

    clf = RandomForestClassifier(n_jobs=-1)
    clf.fit(X_train, y_train)
    print("Training Complete")
    return clf

def messageSimilarity(decryptedMessage, actualMessage):
    diffIndices = [i for i in range(len(decryptedMessage)) if decryptedMessage[i] != actualMessage[i]]
    return (len(decryptedMessage) - len(diffIndices)) / len(decryptedMessage)

if __name__ == "__main__":
    # Train the model
    clf = trainModel()
    # Example encrypted message
    encryptedMessage = "fmz vjbzs lisoh osw zjssu srzi fmz rvon xsk"  # "the quick brown fox jumps over the lazy dog"
    symbolMatchingInit(encryptedMessage)
    decryptedMessage = processMessage(encryptedMessage, clf)
    print("Decrypted message:", decryptedMessage)
    print(f"Message Similarity: {messageSimilarity(decryptedMessage.replace(" ", ""), 'the quick brown fox jumps over the lazy dog'.replace(" ", "")):.2f}%")
