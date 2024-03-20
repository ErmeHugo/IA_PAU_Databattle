import mysql.connector
import re
from sql_info import *
import unicodedata

def remove_unnecessary_tokens(text):
    # Balise HTML
    cleaned_text = re.sub(r'<.*?>', '', text)
    # Manipulation d'affichage
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.replace('\r', '')
    cleaned_text = cleaned_text.replace('\xa0', '')
    cleaned_text = cleaned_text.replace('\x0c', '')
    cleaned_text = cleaned_text.strip()
    return cleaned_text


# Connexion de la base de données MySQL
connection = mysql.connector.connect(
    host=localhost,
    user=root, 
    password=pwd,  #mdp sql perso
    database=db,
    charset ="utf8"
)
cursor = connection.cursor()

# Table et colonnes à extraire
table = "tbldictionnaire"
colonnes = "traductiondictionnaire, codeappelobjet, typedictionnaire"
conditions = f"codelangue = 2 AND typedictionnaire = 'sol'"
ordre = f"codeappelobjet ASC"

requete = f"SELECT {colonnes} FROM {table} WHERE {conditions} ORDER BY {ordre}"

# Nom du fichier de sortie
output_file = "solutions.txt"

# Exécution de la requête SQL et stockage dans un fichier texte
try:
    cursor.execute(requete)
    results = cursor.fetchall()
    with open(output_file, "w", encoding='utf-8') as file:
        for row in results:
            row_list = list(row)
            # Nettoyage du texte
            row_list[0] = remove_unnecessary_tokens(row_list[0])
            # Écriture dans le fichier
            print(row_list, file=file)
    print("Résultats stockés dans", output_file)
    
    import html

    input_file = "solutions.txt"
    output_file = "solutions_traitees.txt"

# Lecture du fichier d'entrée et conversion des entités HTML
    with open(input_file, "r", encoding="utf-8") as f_input:
        lines = f_input.readlines()
        converted_lines = [html.unescape(line) for line in lines]

# Écriture du texte converti dans le fichier de sortie
    with open(output_file, "w", encoding="utf-8") as f_output:
        for line in converted_lines:    
            f_output.write(line)

    print("Conversion des entités HTML terminée. Résultats enregistrés dans", output_file)

        
except mysql.connector.Error as error:
    print("Error executing SQL query:", error)
    
    
finally:
    cursor.close()
    connection.close()
