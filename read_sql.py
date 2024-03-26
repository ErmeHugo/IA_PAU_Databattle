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

codeSolutionsTrouvees = [780] #780 est un bon exemple aussi
codeEtudesDeCasAffilies = []
codeEtudesDeCasI = []

def f1(codeSolutionsTrouvees):
    connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db
)
    cursor = connection.cursor()
    codeEtudesDeCasI = []
    try:
        with connection.cursor() as cursor:
            for i in range(len(codeSolutionsTrouvees)):
                # Requête SQL pour récupérer les colonnes avec codedsolution dans la liste codeSolutionsTrouvees
                sql = "SELECT DISTINCT coderex FROM tblgainrex WHERE codesolution = %s" 

                # Exécution de la requête SQL avec le paramètre a
                cursor.execute(sql, (codeSolutionsTrouvees[i],))
            
                # Récupération des résultats
                result = cursor.fetchall()
                #print(result)

                for j in result:
                    # Ajout des résultats à la liste
                    codeEtudesDeCasI.append(j[0])
                codeEtudesDeCasI.sort()
                codeEtudesDeCasAffilies.append(codeEtudesDeCasI)
                codeEtudesDeCasI = []

    finally:
        # Fermeture de la connexion à la base de données
        connection.close()

    return(codeEtudesDeCasAffilies)


# Connexion de la database aux mysql perso
connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db
)
cursor = connection.cursor()

""" DANS LA TABLE tblrex"""

# / 1877 etudes de cas, on ne prend en compte que 2,3,4,11,12,
# codeuniteenergie = 1 -> NONE              / 752
# codeuniteenergie = 2 -> GJ                / 176
# codeuniteenergie = 3 -> GWh               / 15
# codeuniteenergie = 5 -> kWh               / 288
# codeuniteenergie = 6 -> ...               / 1
# codeuniteenergie = 7 -> litre             / 25
# codeuniteenergie = 9 -> m^3               / 2
# codeuniteenergie = 11 -> MMBtu            / 317
# codeuniteenergie = 12 -> MWh              / 235
# codeuniteenergie = 14 -> tep              / 37
# codeuniteenergie = 15 -> tonnes           / 9
# codeuniteenergie = 16 -> kW               / 4
# codeuniteenergie = 21 -> gallon           / 1
# codeuniteenergie = 22 -> pounds           / 1
# codeuniteenergie = 23 -> therms           / 4
# codeuniteenergie = 30 -> kVA              / 1
# codeuniteenergie = 34 -> %                / 4
# codeuniteenergie = 41 -> kWh/m²           / 5 pris en compte

# codeperiodeenergie = 1 -> NONE            / 581
# codeperiodeenergie = 2 -> ...             / 17
# codeperiodeenergie = 3 -> /an             / 1277
# codeperiodeenergie = 4 -> /jour           / 2

""" DANS LA TABLE tblgainrex # ligne """
# gainfinancierperioderex = 1 -> NONE       / 807
# gainfinancierperioderex = 2 -> ...        / 5
# gainfinancierperioderex = 3 -> /an        / 1065

try:
    with connection.cursor() as cursor:
        # Requête SQL pour récupérer les colonnes avec typedictionnaire = 'sol'
        sql = "SELECT numrex, gesrex FROM tblrex WHERE numrex = 1" #tblrex ligne 1382
        
        # Exécution de la requête SQL
        cursor.execute(sql)
        
        # Récupération des résultats
        result = cursor.fetchall()
        
        # Affichage des résultats
        for row in result:
            print(row)
finally:
    # Fermeture de la connexion à la base de données
    connection.close()


################################## INITIALISER LES LISTES DES BILANS ###################################

# Connexion de la database aux mysql perso
connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db
)
cursor = connection.cursor()


codeEtudesBilans = []
def f2(codeEtudesDeCasAffilies):
    connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db
    )
    cursor = connection.cursor()
    try:
        with connection.cursor() as cursor:
            for i in range(len(codeEtudesDeCasAffilies)):
                codeEtudesBilansI = []  # Initialisation de la liste interne
                
                for j in range(len(codeEtudesDeCasAffilies[i])):
                    # Requête SQL pour récupérer les colonnes avec typedictionnaire = 'sol'
                    sql = "SELECT numrex, gainfinancierrex, codemonnaie, gainfinancierperioderex, energierex, codeuniteenergie, codeperiodeenergie, gesrex FROM tblrex WHERE numrex = %s" #tblrex ligne 1382
            
                    # Exécution de la requête SQL
                    cursor.execute(sql, (codeEtudesDeCasAffilies[i][j],))
            
                    # Récupération des résultats
                    result = cursor.fetchall()

                    for k in result:
                        k = list(k)
                        # Ajout des résultats à la liste
                        codeEtudesBilansI.append(k)
                
                # Ajout de la liste interne à la liste externe
                codeEtudesBilans.append(codeEtudesBilansI)
    finally:
        # Fermeture de la connexion à la base de données
        connection.close()

    return(codeEtudesBilans)

def f3(codeSolutionsTrouvees):
    return f2(f1(codeSolutionsTrouvees))



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
    """row_list = []
    for i in range(len(results)):
        row_list.append(list(results[i]))
        row_list [i][0] = remove_unnecessary_tokens(row_list[i][0])
        row_list [i][0] = clean_tweet(row_list[i][0], flg_stemm=False, flg_lemm=True, lst_stopwords=None)
    print(row_list)"""
    for row in results:
        row_list = list(row)
        row_list[0] = remove_unnecessary_tokens(row_list[0])
        row_list[0] = clean_tweet(row_list[0], flg_stemm=False, flg_lemm=True, lst_stopwords=None)
        # Fonctionne en considérant que la première requête est un texte 
        # Possibilité de travailler avec des dico pour palier à ça
        #print(row_list[0])
        
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
""" 
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
"""