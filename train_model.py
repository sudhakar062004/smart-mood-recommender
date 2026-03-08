import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def train_model():
    # Load dataset
    data = pd.read_csv('dataset/moods.csv')
    
    # Feature extraction
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(data['text'])
    y = data['label']
    
    # Train Naive Bayes model
    model = MultinomialNB()
    model.fit(X, y)
    
    # Save model and vectorizer
    joblib.dump(model, 'mood_model.pkl')
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    print("Model and vectorizer saved successfully!")

if __name__ == "__main__":
    train_model()
