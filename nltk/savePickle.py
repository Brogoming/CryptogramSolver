import nltk
import random
from nltk.corpus import movie_reviews
import pickle

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]

def findFeatures(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# print(findFeatures(movie_reviews.words('neg/cv000_29416.txt')))
featureSets = [(findFeatures(rev), category) for (rev, category) in documents]

training_set = featureSets[:1900]
testing_set = featureSets[1900:]

# posterior = prior occurrences x likelihood/evidence
# classifier = nltk.NaiveBayesClassifier.train(training_set)

# read the naivebayes.pickle
classifier_file = open('naivebayes.pickle', 'rb')
classifier = pickle.load(classifier_file)
classifier_file.close()

print("Naive Bayes Algo accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

# saves the classifier to use for later
# save_classifier = open('naivebayes.pickle', 'wb')
# pickle.dump(classifier, save_classifier)
# save_classifier.close()

# there might be something here I can use but will have to think about it, this does involve saving data for later which I think I could utilize 