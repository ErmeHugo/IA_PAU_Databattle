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
#r

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

# Execution de la requête
try:
    cursor.execute(requete)
    results = cursor.fetchall()
    for row in results:
        row_list = list(row)
        # Fonctionne en considérant que la première requête est un texte 
        # Possibilité de travailler avec des dico pour palier à ça
        row_list [0] = remove_unnecessary_tokens(row_list[0])
        print(row_list)
        
except mysql.connector.Error as error:
    print("Error executing SQL query:", error)
    
finally:
    cursor.close()
    connection.close()
    
    

