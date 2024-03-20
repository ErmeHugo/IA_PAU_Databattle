import mysql.connector
import re
from sql_info import *

def remove_unnecessary_tokens(text):
    # Balise HTML
    cleaned_text = re.sub(r'<.*?>', '', text)
    # Manipulation d'affichage
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.strip()
    return cleaned_text


# Connexion de la database aux mysql perso
connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db
)
cursor = connection.cursor()

# Fichier SQL 
#with open('data.sql', 'r') as file:
#    sql_queries = file.read()

table = "tbldictionnaire"
colonnes = "traductiondictionnaire,codeappelobjet"
conditions = f"codelangue = 2 "#AND codeappelobjet = 719"


requete = f"SELECT {colonnes} FROM {table} WHERE {conditions}"


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


# Execution de la requête
try:
    cursor.execute(requete)
    results = cursor.fetchall()
    row_list = []
    for i in range(len(results)):
        row_list.append(list(results[i]))
        row_list [i][0] = remove_unnecessary_tokens(row_list[i][0])
        row_list [i][0] = clean_tweet(row_list[i][0], flg_stemm=False, flg_lemm=True, lst_stopwords=None)
    print(row_list)
    """for row in results:
        row_list = list(row)
        # Fonctionne en considérant que la première requête est un texte 
        # Possibilité de travailler avec des dico pour palier à ça
        row_list [0] = remove_unnecessary_tokens(row_list[0])
        clean_tweet(row_list[0], flg_stemm=False, flg_lemm=True, lst_stopwords=None)
        print(row_list)"""
        
except mysql.connector.Error as error:
    print("Error executing SQL query:", error)
    
finally:
    cursor.close()
    connection.close()

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
 
 
def extract_keywords(text):
    # Tokenisation du texte
    tokens = word_tokenize(text)
    # Étiquetage des parties du discours
    pos_tags = pos_tag(tokens)
    # Extraction des mots-clés (noms et verbes)
    keywords = [word for word, pos in pos_tags if pos.startswith('N') or pos.startswith('V')]
    return keywords
 
# Exemple d'utilisation
text = "atelier"
keywords = extract_keywords(text)
print("Mots-clés :", keywords)    

for i in range(len(row_list)):
    row_list[i][0] = extract_keywords(row_list[i][0])
#print(row_list)

renvoyer = []

for i in range(len(row_list)):
    for j in range(len(keywords)):
        for k in range(len(row_list[i][0])):
            if keywords[j] == row_list[i][0][k]:
                renvoyer.append(row_list[i])
                print(row_list[i],"\n")
