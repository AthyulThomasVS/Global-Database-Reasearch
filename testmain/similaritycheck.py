from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_descriptions(desc1, desc2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([desc1, desc2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity


