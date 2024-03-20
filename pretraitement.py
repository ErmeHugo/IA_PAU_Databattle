from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Charger le texte nettoyé depuis le fichier
input_file = "solutions_traitees.txt"
output_file = "tokens.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Tokenization
tokens = word_tokenize(text)

# Charger les mots vides pour le français
stop_words = set(stopwords.words('french'))

# Supprimer les mots vides
tokens_without_stopwords = [word for word in tokens if word.lower() not in stop_words]

# Écrire les tokens sans mots vides dans le fichier de sortie
with open(output_file, "w", encoding="utf-8") as f_output:
    for token in tokens_without_stopwords:    
        f_output.write(token + "\n")

# Afficher les tokens sans mots vides
print("Tokens sans mots vides dans :", output_file)