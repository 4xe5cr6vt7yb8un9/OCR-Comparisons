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
def greatest_correct(a, b):
    if (type(a) == str):
        a_list = a.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')
        b_list = b.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')
    else:
        a_list = a
        b_list = b

    length = len(a_list) if len(a_list) < len(b_list) else len(b_list)

    correct = 0
    for i in range(length):
        if a_list[i].strip() == b_list[i].strip():
            correct += 1
        elif length-i > correct:
            far = greatest_correct(a_list[i+1:], b_list[i+1:])
            if far > correct:
                correct = far
            break
        else:
            break

    return correct

def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for i in range(n+1):
        dp[0][i] = i

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[m][n]


if __name__ == "__main__":
    # Test the functions
    
    s1 = 'I Darius Branch, of Castleton in the County of Rutland, and State of Vermont, testify and say, that I was living with my Father in the south east part of Bennington, in the fall of the year 1782, near the residence of Capt. Jonathan Scott, and was present at his house in the early part of Sep- tember (as I think) and saw Samuel Holmes and Sallena Scott united in marriage by Moses Robinson Esq. I cannot recollect the precise day of the month, but distinctly remember that there was a party of tories discovered going through a pasture in the east- erly part of Bennington, which caused the inhabitants to suspect that all was not right; the alarm was immediately given to my Father and others, and a Company of men raised who went in pursuit, and after pur- suing them about eight miles, captur- ed them on the Green Mountain, I think twelve in number, with a Capt. Blakeslee and a negro man whom the tories had taken and were carrying off or leading off to Canada; I was too young to be one of the pursuers, being now in my seventy eighth year, but I am con- fident that Samuel Holmes was one of the party; I was present at the house of Gen. Samuel Safford and saw the Tories when they were brought in by our Troops; I was intimately acquaint-'
    s2 = 'I Darius Branch, of Castleton in the County of Rutland, and State of Vermont, testify and say, that I was living with my Father in the south east part of Bennington in the fall of the year 1782, near the residence of Capt. Jonathan Scott, and was present at his house in the early part of September, (as I think,) and say Samuel Holmes and Sallena Scott united in marriage by Moses Robinson, Esq. I cannot recollect the precise day of the month, but distinctly remember that there was a party of tories discovered going through a pasture in the easterly part of Bennington, which caused the inhabitants to suspect that all was not right; the alarm was immediately given to my Father and others, and a Company of men raised who went in pursuit, and after pursuing them about eight miles, captured them on the Green Mountain, I think twelve in number, with a Capt. Blakeslee and a negro man whom the tories had taken and were carrying off or leading off to Canada; I was too young to be one of the pursuers, being now in my twenty eight year, but am confident that Samuel Holmes was one of the party; I was present at the house of Gen. Samuel Safford and saw the Tories when they were brought in by our Troops; I was intimately acquaint-'

    d1 = "The large dog screamed"
    d2 = "The small dog screamed"

    d = levenshtein_distance(s1, s2)
    print(f"Distance = {d}")

    c = greatest_correct(s1, s2)
    print(f"Most Correct = {c}")