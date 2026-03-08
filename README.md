# Smart Mood-Based Story and Music Recommender

A Flask web application that uses Natural Language Processing (NLP) to detect user mood from text input and recommends a short story and a song with a YouTube link.

## Features
- **Mood Detection**: Uses TF-IDF and Naive Bayes to classify moods: happy, sad, stress, and angry.
- **Personalized Recommendations**: Suggests a story and a song based on the detected mood.
- **Premium UI**: Modern, glassmorphism-inspired design with responsive layout.

## Project Structure
```text
Smart-Mood-Recommender/
├── app.py                  # Flask backend
├── train_model.py          # Model training script
├── mood_model.pkl          # Saved Naive Bayes model
├── tfidf_vectorizer.pkl    # Saved TF-IDF vectorizer
├── dataset/
│   ├── moods.csv           # Training data
│   ├── stories.csv         # Stories database
│   └── songs.csv           # Songs database
├── static/
│   └── style.css           # Premium styling
└── templates/
    ├── index.html          # Main page
    └── result.html         # Results page
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install flask pandas scikit-learn joblib
   ```

2. **Train the Model**:
   (Already trained, but you can re-run if needed)
   ```bash
   python train_model.py
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Web App**:
   Open your browser and go to `http://127.0.0.1:5000`
