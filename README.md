# Smart Mood-Based Story and Music Recommender 🎧📖

An AI-powered web application that detects the user's mood from text input and recommends a motivational story and music to improve emotional well-being.

## 🚀 Features

* **Mood Detection** using Natural Language Processing (TF-IDF + Naive Bayes)
* **Song Recommendation** based on detected mood
* **Story Recommendation** to motivate or calm the user
* **YouTube Integration** for music playback
* **Modern UI** with glassmorphism-inspired responsive design
* **Multiple mood support**: happy, sad, stress, angry

---

## 🛠️ Technologies Used

* Python
* Flask
* Natural Language Processing (NLP)
* Scikit-learn
* Pandas
* HTML, CSS

---

## 📂 Project Structure

Smart-Mood-Recommender/
├── app.py                  # Flask backend
├── train_model.py          # Model training script
├── mood_model.pkl          # Saved Naive Bayes model
├── tfidf_vectorizer.pkl    # Saved TF-IDF vectorizer

dataset/
├── moods.csv               # Training data
├── stories.csv             # Stories database
├── songs.csv               # Songs database

static/
└── style.css               # UI styling

templates/
├── index.html              # Main page
└── result.html             # Results page

---

## ⚙️ Setup Instructions

### 1 Install Dependencies

pip install flask pandas scikit-learn joblib

### 2 Train the Model (Optional)

python train_model.py

### 3 Run the Application

python app.py

### 4 Open the Application

http://127.0.0.1:5000

---

## 💡 Future Improvements

* Add support for **multiple languages**
* Recommend **multiple songs per mood**
* Add **emotion detection using deep learning**
* Deploy the application online

---

## 📌 Author

Sudhakar Reddy
