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
conditions = f"codelangue = 2 AND typedictionnaire = 'sol' AND indexdictionnaire = 1"


requete = f"SELECT {colonnes} FROM {table} WHERE {conditions}"


############################### PRETRAITEMENT ####################################
import string, re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords




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
        # Fonctionne en considérant que la première requête est un texte 
        # Possibilité de travailler avec des dico pour palier à ça
        print(row_list[0])
        
except mysql.connector.Error as error:
    print("Error executing SQL query:", error)
    
finally:
    cursor.close()
    connection.close()

