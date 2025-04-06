import random
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from nltk import FreqDist, bigrams, trigrams
from nltk.corpus import brown
import re
import pickle

englishVocab = set(word.lower() for word in brown.words() if re.search("(?=.*[aeiou])[a-z']+",word))
englishVocab.add('a')
englishVocab.add('i')
englishVocab = sorted(englishVocab, key=len)

freqWordDist = FreqDist(word.lower() for word in brown.words() if re.search("(?=.*[aeiou])[a-z']+",word))
freqWordDist = [word.lower() for word, v in sorted(freqWordDist.items(), key=lambda item: item[1], reverse=True)]

def symbolMatchingInit(inputMessage):
    symbolMatch = {}
    msgCopy = inputMessage.replace(" ", "")
    for symbol in list(msgCopy):
        if symbol not in symbolMatch.keys():
            symbolMatch[symbol] = "_"
    return symbolMatch

def createFeatureList(word, char, index):
    features = []
    charIndex = word.index(char)

    # 1. Letter Frequencies of the word(normalized count)
    charFreqs = FreqDist(word)
    charTotal = sum(charFreqs.values())
    charFreqsNormalized = {char: count / charTotal for char, count in charFreqs.items()}
    charFreq = charFreqsNormalized.get(char, 0)  # Get normalized frequency for this letter
    features.append(charFreq)

    # 2. Bigram Frequencies
    wordBigrams = list(bigrams(word))
    bigramFreqs = FreqDist(wordBigrams)
    bigram = tuple(word[charIndex - 1:charIndex + 1]) if charIndex > 0 else None
    bigramFreq = bigramFreqs[bigram] / len(wordBigrams) if bigram and len(wordBigrams) > 0 else 0
    features.append(bigramFreq)

    # 3. Trigram Frequencies
    wordTrigrams = list(trigrams(word))
    trigramFreqs = FreqDist(wordTrigrams)
    trigram = tuple(word[charIndex - 2:charIndex + 1]) if charIndex > 1 else None
    trigramFreq = trigramFreqs[trigram] / len(wordTrigrams) if trigram and len(wordTrigrams) > 0 else 0
    features.append(trigramFreq)

    # 4. Word Shape (e.g., _e__o for "hello")
    wordShape = ''.join('_' if c.isalpha() else c for c in word)

    # Use number of underscores as the feature for word shape
    wordShapeUnderscoreCount = wordShape.count('_')
    features.append(wordShapeUnderscoreCount)

    # 5. Letter index (First, Middle, Last)
    features.append(index)

    # Return the feature vector
    return features

def getAvailableWords(word, symbolMatch):
    availWords = [t for t in freqWordDist if len(t) == len(word)]
    if any(symbol in symbolMatch.keys() for symbol in list(word)):
        for s, symbol in enumerate(word):
            if symbolMatch[symbol] != "_":
                availWords = [w for w in availWords if w[s] == symbolMatch[symbol]]
    return availWords

def processMessage(cipherText, model):
    symbolMatch = symbolMatchingInit(cipherText)
    decrypted = []
    message = cipherText.split(" ")
    random.shuffle(message)

    for word in message:
        for s, symbol in enumerate(word):
            availWords = getAvailableWords(word, symbolMatch)
            if len(availWords) == 0:
                continue

            if symbol.isalpha() and symbolMatch[symbol] == '_':
                features = createFeatureList(word, symbol, s)
                prediction = str(model.predict([features])[0])

                availLetters = [t[s] for t in availWords if t[s].isalpha()]
                letterFreq = FreqDist(availLetters)
                while prediction in list(symbolMatch.values()) or prediction == symbol or not prediction.isalpha() or prediction not in availLetters:
                    if len(letterFreq) > 0:
                        prediction = random.choices(list(letterFreq.keys()), list(letterFreq.values()), k=1)[0]
                        letterFreq.pop(prediction)
                    else:
                        prediction = '_'  # Use a placeholder or fallback letter
                        break
                symbolMatch[symbol] = str(prediction)

    for symbol in cipherText:
        if symbol in symbolMatch.keys():
            decrypted.append(symbolMatch[symbol])
        else:
            decrypted.append(symbol)

    return "".join(decrypted)

def trainModel(modelName, modelType, nEstimators, randomness, numSent):
    X_train = []
    y_train = []
    model = None

    # Create training data using random ciphers
    sents = [" ".join(s).lower() for s in brown.sents()]
    if len(sents) != numSent:
        sents = sents[:numSent]

    for sent in sents:  # Generate multiple samples
        for i, word in enumerate(sent.split(" ")):
            for l, letter in enumerate(word):
                if letter.isalpha():  # Only use letters as valid data points
                    X_train.append(createFeatureList(word, letter, l))
                    y_train.append(letter)  # Corresponding plaintext letter

    if modelType == 'RandomForestClassifier':
        model = RandomForestClassifier(n_jobs=-1, n_estimators=nEstimators, random_state=randomness, max_features=None)
    elif modelType == 'GradientBoostingClassifier':
        model = GradientBoostingClassifier(n_estimators=nEstimators, random_state=randomness, max_features=None)
    elif modelType == 'LogisticRegression':
        model = LogisticRegression(n_jobs=-1, max_iter=nEstimators, random_state=randomness)

    model.fit(X_train, y_train)
    pickle.dump(model, open(f'models/{modelName}.sav', 'wb'))
    return model

def loadModel(modelFile):
    model = pickle.load(open(modelFile, 'rb'))
    return model

def scoreMessage(decryptedMessage, encryptedMessage):
    messagePoint = 0
    if len(decryptedMessage) != len(encryptedMessage) or '_' in decryptedMessage:
        return 0
    for word in decryptedMessage.split(" "):
        if word in englishVocab:
            messagePoint += 1
    return messagePoint/len(decryptedMessage.split(" "))

    # kpf jccmy bif cu oeif
    # p yxx dprexe ar uv spre
    # u kqudn kqc wcjk lhjjuwac hvkyhoc qfj bck kh wc jccd