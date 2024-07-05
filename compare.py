import nltk
from nltk import download
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 

import gensim.downloader as api

# Calculates Word distance but very slow
def word_distance(sentences):
    nltk.download('all', quiet=True)

    # downloading stopwords
    download('stopwords', quiet=True)
    stopword = stopwords.words('english')

    # initializing lemmatizer
    lemmatizer = WordNetLemmatizer()

    model = api.load('word2vec-google-news-300')

    # cleaning text by removing stopwords and 
    # getting the root word of words using lemmatiztion
    def preprocess(sentences):
        new_sentences = []
        for sent in sentences:
            sent = [lemmatizer.lemmatize(w) for w in sent.lower().split() if w not in stopword]
            new_sentences.append(sent)
        return new_sentences

    # prerocessing the senteces
    sentences = preprocess(sentences)
    distance = model.wmdistance(sentences[0], sentences[1])
    return distance

# Calculates the cosine similarity between two sentences
def cos_similarity(a, b):
    a_list = word_tokenize(a)
    b_list = word_tokenize(b)

    sw = stopwords.words('english')
    keyA = []
    keyB = []

    a_set = {w for w in a_list if not w in sw}
    b_set = {w for w in b_list if not w in sw}

    rvector = a_set.union(b_set)
    for word in rvector:
        if word in a_set: keyA.append(1)
        else: keyA.append(0)
        if word in b_set: keyB.append(1)
        else: keyB.append(0)

    c = 0

    for i in range(len(rvector)):
        c += keyA[i] * keyB[i]

    cosine = c / float((sum(keyA) * sum(keyB)) ** 0.5)
    return cosine

# Calculates the percentage of correct words that are in the correct spot
def percentage_correct(a, b):
    a_list = a.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')
    b_list = b.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')

    length = len(a_list) if len(a_list) < len(b_list) else len(b_list)

    correct = 0
    for i in range(length):
        if a_list[i].strip() == b_list[i].strip():
            correct += 1
        else:
            break

    return correct