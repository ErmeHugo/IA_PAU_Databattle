########### Import librairies ###########
import tensorflow as tf
import numpy as np
import mysql.connector
import re
import copy

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sql_info import *
from Fonction_Camembert import *


########### LIAISON BDD PYTHON ###########


# Connexion de la database aux mysql perso
connection = mysql.connector.connect(
    host=db,
    user=root, 
    password=pwd,  
    database=db
)
cursor = connection.cursor()

table = "tbldictionnaire"
colonnes = "codeappelobjet,traductiondictionnaire"
conditions = f"codelangue = 2 AND typedictionnaire = 'sol' AND indexdictionnaire = 1"#AND codeappelobjet = 719

requete = f"SELECT {colonnes} FROM {table} WHERE {conditions}"

# Execution de la requête
try:
    cursor.execute(requete)
    results = cursor.fetchall()
    dict_sol = {}
    for row in results:
        # En considérant que le premier terme est le codeappelobjet
        # Création d'un dictionnaire reliant solution à son texte 
        if row[0] in dict_sol :
            dict_sol[row[0]].append(row[1])
        else : 
            dict_sol[row[0]] = [row[1]]
    for key,item in dict_sol.items():
        text = " ".join(item)
        dict_sol[key] = text

except mysql.connector.Error as error:
    print("Error executing SQL query:", error)

finally:
    cursor.close()
    connection.close()


########### PRÉTRAITEMENT BDD ###########


dict_sol_copy = copy.deepcopy(dict_sol)

for key,text in dict_sol.items():
    #text = remove_punctuation(text)
    text = remove_unnecessary_tokens(text)
    lemmatized_text = custom_lemmatize(text)
    dict_sol[key] = ""
    dict_sol[key] = " ".join(lemmatized_text)



########### MODELE ###########

model =  SentenceTransformer("dangvantuan/sentence-camembert-large")

# Charger les embeddings à partir du fichier
calculate_and_save_embeddings(model, dict_sol)
dict_embeddings = joblib.load('embeddings.pkl')

# Utilisation de la fonction pour trouver les textes les plus pertinents pour une question spécifique
question = "C'est quoi la HP flottante ?"
find_top_texts(question, model, dict_embeddings, dict_sol_copy)

question_2 = "Je voudrais dimensionner un panneau solaire."
find_top_texts(question_2, model, dict_embeddings, dict_sol_copy)

question_3 = "Quel gain pour un variateur de vitesse ?"
find_top_texts(question_3, model, dict_embeddings, dict_sol_copy)

question_4 = "Quelles sont les meilleures solutions pour l'agro-alimentaire ? "
find_top_texts(question_4, model, dict_embeddings, dict_sol_copy)

