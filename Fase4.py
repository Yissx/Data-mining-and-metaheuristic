# -*- coding: utf-8 -*-
"""
@author:
    Nancy Yissel Cuellar Valdivia
    Andrea De Santiago Legaspi
    Valeria Macías Soto
    Montserrat Alejandra Ulloa Rivera
"""
# pip install TextBlob
# pip install nltk
# pip install bs4
# pip install autocorrect
# pip install vaderSentiment
# pip install WordCloud

# Lbrerías de Python.
print("Preprocesando datos")
from textblob import TextBlob
from autocorrect import spell
from string import punctuation
import pandas as pd
import re
import emoji
import csv
# import clean.cleaner as c
# import process.processing as p
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# from nltk.stem import SnowballStemmer
# nltk.download()
# nltk.download('punkt')
# nltk.download("wordnet")
# nltk.download('stopwords')

# Diccionario de contracciones en inglés
contractions_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I had",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "iit will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they had",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

# 1. Mensajes de Twitter para Escanear.
data = pd.read_csv("Limpios/56.csv")
data


# 2. Remueve Contracciones.
def expand_contractions(text, contractions_dict):
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        # first_char = match[0]
        expanded_contraction = contractions_dict.get(match) \
            if contractions_dict.get(match) \
            else contractions_dict.get(match.lower())
        expanded_contraction = expanded_contraction
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


# 3. Remove Tags and URL
def remove_Tags(text):
    global cleaned_text
    tags = r'<[^>]+>'  # HTML tags
    mencion = r'(?:@[\w_]+)'  # @-Mención
    # hashtag = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" #Hash-tags
    # pattern = r'(https|http):\/\/([^\/]+)\/(\w+(?:\.\w+)+||$)'
    urls = r'https[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'  # URLs
    # pattern = r'(https|http):\/\/([^\/]+)\/(\w+(?:\.\w+)+||$)'
    m = re.findall(tags, text)
    m2 = re.findall(mencion, text)
    # m3 = re.findall(hashtag, text)
    m4 = re.findall(urls, text)
    # m5 = re.findall(pattern, text)
    # print(m4)

    for tok in m:
        text = text.replace(tok, "tags")
    for toke in m2:
        text = text.replace(toke, "mencion")
    # if m3:
    #    text = text.replace(m3.group(0), "hashtag")
    for token in m4:
        text = text.replace(token, "URL")
    # if m5:
    #    text = text.replace(m5.group(0), "URL")

    return emoji.get_emoji_regexp().sub(r'', text)


# 4. Remove Numbers
def remove_numbers(text):
    output = ''.join(c for c in text if not c.isdigit())
    return output


# 5. Remove punctuation
def remove_punct(text):
    return ''.join(c for c in text if c not in punctuation)


# 6. Spell Check
def autospell(text):
    spells = [spell(w) for w in (nltk.word_tokenize(text))]
    return " ".join(spells)


# 7. Convert text to lower case:
def to_lower(text):
    """
    Converting text to lower case as in, converting "Hello" to  "hello" or "HELLO" to "hello".
    """
    return ' '.join([w.lower() for w in nltk.word_tokenize(text)])


# 8. Stopwords
stop_words = set(stopwords.words('english'))


def remove_stopwords(sentence):
    clean_sent = []
    for w in word_tokenize(sentence):
        if not w in stop_words:
            clean_sent.append(w)
    return " ".join(clean_sent)


# 9. Lemmatize
# ss = SnowballStemmer('english')
wl = WordNetLemmatizer()


def lemmatize(text):
    word_tokens = nltk.word_tokenize(text)
    lemmatized_word = [wl.lemmatize(word) for word in word_tokens]
    # stemmed_word = [ss.stem(word) for word in lemmatized_word]
    return " ".join(lemmatized_word)


# 10. Remove duplicate words
def remove_duplicate(sentence):
    resultantList = []
    for element in word_tokenize(sentence):
        if element not in resultantList:
            resultantList.append(element)
    return " ".join(resultantList)


def pre_process(text):
    """
    """
    text = expand_contractions(text, contractions_dict)
    text = remove_Tags(text)
    text = remove_numbers(text)
    text = remove_punct(text)
    # text = autospell(text)
    text = to_lower(text)
    text = remove_stopwords(text)
    text = lemmatize(text)
    text = remove_duplicate(text)
    # 11. Tokenizar tweet
    text = TextBlob(text).words
    return (text)


pre_process_tweet = []
for tweet in data['tweet_text']:
    element = pre_process(tweet)
    pre_process_tweet.append(element)

pre_process_tweet

# Inigrams
print("N-GRAMS")
for tweet in pre_process_tweet:
    unigrams = list(nltk.ngrams(tweet, 1))
    print(unigrams)
    print("-------------------------------------------------")

# Bigrams
for tweet in pre_process_tweet:
    bigrams = list(nltk.ngrams(tweet, 2))
    print(bigrams)
    print("-------------------------------------------------")

# Trigrams
for tweet in pre_process_tweet:
    trigrams = list(nltk.ngrams(tweet, 3))
    print(trigrams)
    print("-------------------------------------------------")

# Análisis del sentimiento del tweet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
fname = "Preprocesados/56-1"
with open('%s.csv' % (fname), 'w', encoding="utf-8") as file:
    w = csv.writer(file)
    w.writerow(['polaridad', 'subjetividad', 'sentimiento', 'word_count'])
    for tweet in pre_process_tweet:
        cont = 0;
        for i in tweet:
            cont = cont + 1
        sentence = str(tweet)
        vs = analyzer.polarity_scores(sentence)
        # print("{:-<65} {}".format(sentence, str(vs)))
        valores = []
        for key in vs:
            valores.append(vs[key])
        rs = valores[3]
        sentimiento = round(rs)
        # print(sentimiento)
        sub = TextBlob(sentence).sentiment.subjectivity

        if sentimiento == 1:
            tweet = "pos"
        if sentimiento == 0:
            tweet = "neu"
        if sentimiento == -1:
            tweet = "neg"
        # print(tweet)

        w.writerow([rs,
                    sub,
                    tweet,
                    cont])
# print(process_tweet)