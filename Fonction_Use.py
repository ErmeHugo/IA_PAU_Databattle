import spacy
import fr_core_news_md
import re
import io

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from spacy.lang.fr import French

nlp = fr_core_news_md.load()

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

def remove_unnecessary_tokens(text):
    # Balise HTML
    cleaned_text = re.sub(r'<.*?>', ' ', text)
    # Manipulation d'affichage
    cleaned_text = cleaned_text.replace('\n', ' ')
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def chunk_text(text, chunk_size=500000):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size
        return chunks