#Prérequis : 
#
# python3 -m spacy download fr_core_news_md

import spacy
import fr_core_news_md
import re
import io

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from spacy.lang.fr import French

nlp = fr_core_news_md.load()  #A installer before 

########## FONCTIONS INTERMEDIAIRES ###########


##########                          ###########
def custom_lemmatize(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    return lemmas


#spaCy n'accepte pas les textes de plus de  100.000 lignes
#Or le nôtre est composé de +124.000
#Donc il faut découper le texte en plusieurs (chunks)
def chunk_text(text, chunk_size=500000):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
    return chunks

def remove_punctuation(text):
    # Supprimer la ponctuation tout en conservant les chiffres
    return re.sub(r'[^\w\s\d]', '', text)








########### PRETRAITEMENT ###########


###########               ###########
#Attribution et chargement des fichiers d'entrée, intermédiaire et final, et lecture
input_file = "solutions_traitees.txt"
inter_file = "tokens_lemmatises.txt"
output_file = "tokens.txt"
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()


#Ratio la ponctuation
text_without_punctuation = remove_punctuation(text)

#On chunk
text_chunks = chunk_text(text_without_punctuation)

# Lemmatisation des morceaux de texte avec spaCy
tokens_lemmatises = []
for chunk in text_chunks:
    tokens_lemmatises.extend(custom_lemmatize(chunk))

# Écrire les tokens lemmatisés dans le fichier de sortie
with open(inter_file, "w", encoding="utf-8") as f_output:
    for token in tokens_lemmatises:
        f_output.write(token + "\n")
print("Tokens lemmatisés dans :", inter_file)   


# Supprimer les mots vides
stop_words = set(nlp.Defaults.stop_words)
tokens_sans_stopwords = [word for word in tokens_lemmatises if word.lower() not in stop_words]

# Écrire les tokens sans mots vides dans le fichier de sortie
with open(output_file, "w", encoding="utf-8") as f_output:
    for token in tokens_sans_stopwords:    
        f_output.write(token + "\n")
print("Tokens sans mots vides dans :", output_file)



######### MODELE WORD2VEC ET TEST ##########


#########                         #########

# Entraînement du modèle Word2Vec
model = Word2Vec(sentences=[tokens_sans_stopwords], vector_size=100, window=5, min_count=1, workers=4, epochs=10)
weights = model.wv.vectors
vocab = model.wv.index_to_key


# Mots similaires
mots_similaires = model.wv.most_similar('variateur')
print("\nMots similaires à 'variateur':", mots_similaires)

out_v = io.open('vectors.tsv', 'w', encoding='utf-8')
out_m = io.open('metadata.tsv', 'w', encoding='utf-8')


for index, word in enumerate(vocab):
  if index == 0:
    continue  # skip 0, it's padding.
  vec = weights[index]
  out_v.write('\t'.join([str(x) for x in vec]) + "\n")
  out_m.write(word + "\n")
out_v.close()
out_m.close()

"""Download the `vectors.tsv` and `metadata.tsv` to analyze the obtained embeddings in the [Embedding Projector](https://projector.tensorflow.org/):"""

try:
  from google.colab import files
  files.download('vectors.tsv')
  files.download('metadata.tsv')
except Exception:
  pass
