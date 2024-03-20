########################## LIBRAIRIES ########################################

import mysql.connector
import re
from sql_info import *
from read_sql import *

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np


################################################################################

gpus = tf.config.list_physical_devices('GPU')

if gpus:
    try:
        #Currenlty memory growth needs to be the same across GPUs
        for gpu in gpus :
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical devices", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


imdb_data = row_list
print(imdb_data)

############################### PRETRAITEMENT ####################################
import string, re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from tqdm import tqdm
import os

stop_words =set(stopwords.words('french'))


# suppresion de la ponctuation, passage en minuscule, stemming, lemmatisation, stopwords

def clean_tweet(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    """
    Cette fonction va nettoyer le texte :
    + mettre en minuscule,
    + supprimer un certain nombre d'expression,
    + choix lemmatisation / stemming,
    + choix d'une liste de stopwords
    """

    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
    text = re.sub(r"(\s\-\s|-$)", "", text)
    text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
    text = re.sub(r"\&\S*\s", "", text)
    text = re.sub(r"\&", "", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\#", "", text)
    text = re.sub(r"\$", "", text)
    text = re.sub(r"\£", "", text)
    text = re.sub(r"\%", "", text)
    text = re.sub(r"\:", "", text)
    text = re.sub(r"\@", "", text)
    text = re.sub(r"\-", "", text)

    ## transforme en tokens
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in

                    lst_stopwords]

    ## Stemming (supprime -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    ## Lemmatisation (retourne la racine du mot)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    ## liste => string
    text = " ".join(lst_text)
    return text

for i in range (len(results)):
    imdb_data[2][i] = clean_tweet(imdb_data[0][i], flg_stemm=False, flg_lemm=True, lst_stopwords=stop_words)




import io
import re
import string
import tqdm

import numpy as np

import tensorflow as tf
from keras import layers

%load_ext tensorboard

SEED = 42
AUTOTUNE = tf.data.AUTOTUNE




















