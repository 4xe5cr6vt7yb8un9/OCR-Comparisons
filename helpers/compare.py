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

# Uses Matrix math to find the levenshtein distance between two sentences
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

# Calculates greatest number of correct words in a row
def greatest_correct(s1, s2):
    a_list = s1.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')
    b_list = s2.replace(',', '').replace('- ', '').replace('-', ' ').split(' ')

    a_list = [i for i in a_list if i]
    b_list = [i for i in b_list if i]

    greatest = 0

    while (len(a_list) > greatest):
        count = great2(a_list, b_list)

        if count > greatest:
            greatest = count

        if (count == 0 or count == 1):
            count += 1

        a_list = a_list[count:]

    return greatest
        

def great2(a_list, b_list):
    b = " ".join(i for i in b_list)
    matche = ""

    count = 0
    for a in a_list:
        count += 1
        matche = " ".join([matche, a])

        f = b.count(matche.strip())
        if f == 0:
            return count-1

    return count


if __name__ == "__main__":
    # Test the functions
    
    s1 = 'I Darius Branch, of Castleton in the County of Rutland, and State of Vermont, testify and say, that I was living with my Father in the south east part of Bennington, in the fall of the year 1782, near the residence of Capt. Jonathan Scott, and was present at his house in the early part of Sep- tember (as I think) and saw Samuel Holmes and Sallena Scott united in marriage by Moses Robinson Esq. I cannot recollect the precise day of the month, but distinctly remember that there was a party of tories discovered going through a pasture in the east- erly part of Bennington, which caused the inhabitants to suspect that all was not right; the alarm was immediately given to my Father and others, and a Company of men raised who went in pursuit, and after pur- suing them about eight miles, captur- ed them on the Green Mountain, I think twelve in number, with a Capt. Blakeslee and a negro man whom the tories had taken and were carrying off or leading off to Canada; I was too young to be one of the pursuers, being now in my seventy eighth year, but I am con- fident that Samuel Holmes was one of the party; I was present at the house of Gen. Samuel Safford and saw the Tories when they were brought in by our Troops; I was intimately acquaint-'
    s2 = 'I Darius Branch, of Castleton in the County of Rutland, and State of Vermont, testify and say, that I was living with my Father in the south east part of Bennington in the fall of the year 1782, near the residence of Capt. Jonathan Scott, and was present at his house in the early part of September, (as I think,) and say Samuel Holmes and Sallena Scott united in marriage by Moses Robinson, Esq. I cannot recollect the precise day of the month, but distinctly remember that there was a party of tories discovered going through a pasture in the easterly part of Bennington, which caused the inhabitants to suspect that all was not right; the alarm was immediately given to my Father and others, and a Company of men raised who went in pursuit, and after pursuing them about eight miles, captured them on the Green Mountain, I think twelve in number, with a Capt. Blakeslee and a negro man whom the tories had taken and were carrying off or leading off to Canada; I was too young to be one of the pursuers, being now in my twenty eight year, but am confident that Samuel Holmes was one of the party; I was present at the house of Gen. Samuel Safford and saw the Tories when they were brought in by our Troops; I was intimately acquaint-'

    d1 = "The large dog screamed"
    d2 = "The small dog screamed"

    t1 = "WIDOW, &c. File No. 10476 Hannah Burns Formerly wife of James Hodge Prvt Rev. War Act: Feby 3rd 1853 Index: -- Vol. a, Page 102 [Arrangement of 1870.]"
    t2 = "Roy WIDOW, &c.  File No. 12756 Hannah Burns James, Wid. James Hodge Dist  ___ War  Act: July 27, 1868  Index.�Vol. A     Page 102  [Arrangement of 1870.]"

    c1 = 'I Darius Branch, of Castleton in the County of Rutland, and State of Vermont, testify and say'
    c2 = 'I Darius Branch, of Castleton in the County of Rutland, and State of eVermont, testify and say'

    #d = levenshtein_distance(s1, s2)
    #print(f"Distance = {d}")

    c = greatest_correct(s1, s2)
    print(f"Most Correct = {c}")