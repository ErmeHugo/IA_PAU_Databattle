import tensorflow as tf
from transformers import TFAutoModel, AutoTokenizer
import numpy as np
import mysql.connector
import re
from sql_info import *
from Fonction_Use import *

########### LIAISON BDD PYTHON ##############


# Connexion de la database aux mysql perso
connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  
    database=db
)
cursor = connection.cursor()

table = "tbldictionnaire"
colonnes = "codeappelobjet,traductiondictionnaire"
conditions = f"codelangue = 2 AND typedictionnaire = 'sol'"#AND codeappelobjet = 719

requete = f"SELECT {colonnes} FROM {table} WHERE {conditions}"

# Execution de la requête
try:
    cursor.execute(requete)
    results = cursor.fetchall()
    dict_sol = {}
    for row in results:
        # En considérant que le premier terme est le codeappelobjet
        # Création d'un dictionnaire reliant solution à son texte 
        if f'{row[0]}' in dict_sol :
            dict_sol[row[0]] += "" + row[1]
        else : 
            dict_sol[row[0]] = row[1]
    
        
except mysql.connector.Error as error:
    print("Error executing SQL query:", error)
    
finally:
    cursor.close()
    connection.close()


########### PRÉTRAITEMENT BDD ##############


for key,text in dict_sol.items():
    #text = remove_punctuation(text)
    text = remove_unnecessary_tokens(text)
    lemmatized_text = custom_lemmatize(text)
    dict_sol[key] = ""
    dict_sol[key] = " ".join(lemmatized_text)

#for key in dict_sol:
#    print(f"{key} :",dict_sol[key])

"""
taille_max = 512
dict_sol_1 = {k: dict_sol[k] for k in range(taille_max) if k in dict_sol}
dict_sol_2 = {k: dict_sol[k] for k in range(taille_max,2*taille_max) if k in dict_sol}
dict_sol_3 = {k: dict_sol[k] for k in range(2*taille_max,1089) if k in dict_sol}

for i in range(2,512):
    if i in dict_sol:
        print(f"{i} :",len(dict_sol_1[i]))
"""

########### MODEL  ##############



# Question
question = "Quel gain pour un variateur de vitesse ?"

# Tokenizer et Model BERT
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-french-europeana-cased")
model = TFAutoModel.from_pretrained("dbmdz/bert-base-french-europeana-cased")


# Récupération embedding question
inputs = tokenizer(question, return_tensors='tf')
question_embedding = model(inputs)[1]

# Bert ne peut recevoir plus de 512 entrées donc on subdivise 
# Création des dictionnaires de taille max = 512
taille_max = 512
dict_sol_1 = {k: dict_sol[k] for k in range(taille_max-1) if k in dict_sol}
dict_sol_2 = {k: dict_sol[k] for k in range(taille_max-1,2*taille_max-1) if k in dict_sol}
dict_sol_3 = {k: dict_sol[k] for k in range(2*taille_max-1,1089) if k in dict_sol}

print(len(dict_sol_1))
print(len(dict_sol_2))
print(len(dict_sol_3))

# Calcul des similarités avec chaque texte
similarities = {}


for num_texte, texte in dict_sol.items():
    # Creation des chunks de texte qui se chevauchent
    text_chunks = chunk_text(text)
    
    total_similarity = 0
    
    # Calcul similarité pour chaque chunk
    for chunk in text_chunks:
        # Encodage du chunk
        inputs_texte = tokenizer(chunk, return_tensors='tf')
        texte_embedding = model(inputs_texte)[1]
        
        # Calcul cosine similarity 
        cosine_similarity = np.dot(question_embedding.numpy(), texte_embedding.numpy().T) / (
            np.linalg.norm(question_embedding.numpy()) * np.linalg.norm(texte_embedding.numpy()))
        
        # Accumulate similarity scores
        total_similarity += cosine_similarity.item()
    
    if len(text_chunks) != 0:
        average_similarity = total_similarity / len(text_chunks)
    else:
        average_similarity = 0
    similarities[num_texte] = average_similarity


# Tri des textes par similarité décroissante
sorted_texts = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# Affichage des numéros des textes les plus pertinents
top_texts = sorted_texts[:7]  # Vous pouvez ajuster le nombre de textes à afficher
print("Textes les plus pertinents pour la question:", question)
for num_texte, similarity in top_texts:
    print("Numéro de texte:", num_texte, "- Similarité:", similarity)
    print("Texte associé:", dict_sol[num_texte])
    print()
