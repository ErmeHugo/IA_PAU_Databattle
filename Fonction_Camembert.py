import spacy
import fr_core_news_md
import re
import io
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from spacy.lang.fr import French

nlp = fr_core_news_md.load()

def custom_lemmatize(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    return lemmas

def chunk_text(text, max_chunk_length=50):
    chunks = []
    for i in range(0, len(text), max_chunk_length):
        chunk = text[i:i+max_chunk_length]
        chunks.append(chunk)
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

def find_top_texts(question, model, dict_embeddings, dict_sol, top_n=5):
    # Calculer les embeddings pour la question
    question_embedding = model.encode(question)

    # Calculer la similarité entre la question et chaque phrase
    similarities = {key: cosine_similarity([question_embedding], [dict_embeddings[key]])[0][0] for key in dict_embeddings}

    # Affichage des numéros des textes les plus pertinents
    sorted_texts = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    top_texts = sorted_texts[:top_n] 

    # Récupérer les textes correspondant aux numéros de texte
    texts_and_similarities = []
    for num_texte, similarity in top_texts:
        texte = dict_sol[num_texte]  # Récupérer le texte associé au numéro de texte
        texts_and_similarities.append((num_texte, similarity, texte))  # Ajouter le texte et la similarité à la liste
    print(question)
    return print(texts_and_similarities)


# Calculer et sauvegarder les embeddings en amont
def calculate_and_save_embeddings(model, dict_sol):
    dict_embeddings = {}
    for key, sentence in dict_sol.items():
        dict_embeddings[key] = model.encode(sentence)
    joblib.dump(dict_embeddings, 'embeddings.pkl')
