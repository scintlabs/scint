from typing import overload

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


@overload
def preprocess(word):
    word = word.lower()
    if word.isalpha() and word not in stop_words:
        return lemmatizer.lemmatize(word)
    return None


@overload
def preprocess(sentence):
    words = word_tokenize(sentence)
    preprocessed_words = [preprocess(word) for word in words]
    return " ".join([word for word in preprocessed_words if word])


@overload
def preprocess(document):
    return [preprocess(sentence) for sentence in document]
