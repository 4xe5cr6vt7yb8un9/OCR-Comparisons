import nltk
from nltk import download
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
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