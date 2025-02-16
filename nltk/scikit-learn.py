import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

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
classifier = nltk.NaiveBayesClassifier.train(training_set)

# read the naivebayes.pickle
# classifier_file = open('naivebayes.pickle', 'rb')
# classifier = pickle.load(classifier_file)
# classifier_file.close()

print("Original Naive Bayes Algo accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set))*100)

# Multinomial Naive Bayes
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("Multinomial Naive Bayes accuracy percent: ", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

# # Gaussian Naive Bayes
# GNB_classifier = SklearnClassifier(GaussianNB())
# GNB_classifier.train(training_set)
# print("Gaussian Naive Bayes accuracy percent: ", (nltk.classify.accuracy(GNB_classifier, testing_set))*100)

# Bernoulli Naive Bayes
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("Bernoulli Naive Bayes accuracy percent: ", (nltk.classify.accuracy(BNB_classifier, testing_set))*100)

# LogisticRegression, SGDClassifier, SVC, LinearSVC, NuSVC
# SVC = support vector machines classifier

# Logistic Regression
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression accuracy percent: ", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

# SGD
SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(training_set)
print("SGDClassifier accuracy percent: ", (nltk.classify.accuracy(SGD_classifier, testing_set))*100)

# SVC
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC accuracy percent: ", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

# LinearSVC
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC accuracy percent: ", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

# NuSVC
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC accuracy percent: ", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

# would like to use this but I'm not sure because then I would have to learn another library and idk if I have the time
# for that plus adding this would make it more complex, something I know I'll get frustrated with because I don't understand