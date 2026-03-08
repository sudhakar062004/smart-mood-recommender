from flask import Flask, request, render_template, session, redirect, url_for
from urllib.parse import urlparse, parse_qs, quote_plus
import pandas as pd
import joblib
import random
from spotify_helper import get_dynamic_songs

app = Flask(__name__)
app.secret_key = 'mood-recommender-secret-2024'

# Load model and vectorizer
model = joblib.load('mood_model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')

def extract_video_id(url):
    """Pull the video ID from a YouTube URL."""
    try:
        parsed = urlparse(url)
        if parsed.hostname in ('youtu.be',):
            return parsed.path[1:]
        if parsed.hostname in ('www.youtube.com', 'youtube.com'):
            return parse_qs(parsed.query).get('v', [None])[0]
    except Exception:
        pass
    return None

def build_links(title):
    """Build verified working music search URLs for a song title."""
    q = quote_plus(title)
    return {
        'spotify'  : f'https://open.spotify.com/search/{q}',
        'jiosaavn' : f'https://www.jiosaavn.com/search/{q}',
        'gaana'    : f'https://gaana.com/search/songs?searchQuery={q}',
        'ytmusic'  : f'https://music.youtube.com/search?q={q}',
        'youtube'  : f'https://www.youtube.com/results?search_query={q}',
    }

def load_data():
    stories = pd.read_csv('dataset/stories.csv')
    songs   = pd.read_csv('dataset/songs.csv')
    for col in ['mood', 'language']:
        stories[col] = stories[col].str.strip().str.lower()
        songs[col]   = songs[col].str.strip().str.lower()
    songs['video_id'] = songs['youtube_link'].apply(extract_video_id)
    return stories, songs

def enrich_songs(song_list):
    """Add pre‑built search links to every song dict."""
    for song in song_list:
        song.update(build_links(song['song_title']))
    return song_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    stories, songs = load_data()

    mood_type     = request.form.get('mood_type', 'happy')
    selected_lang = request.form.get('language', 'english').strip().lower()

    if mood_type == 'custom':
        user_input  = request.form.get('mood_text', '')
        input_tfidf = tfidf.transform([user_input])
        prediction  = model.predict(input_tfidf)[0].lower()
    else:
        prediction = mood_type.lower()

    mood_stories = stories[(stories['mood'] == prediction) & (stories['language'] == selected_lang)]
    mood_songs   = songs[(songs['mood'] == prediction) & (songs['language'] == selected_lang)]

    if mood_stories.empty:
        mood_stories = stories[stories['mood'] == prediction]
    if mood_songs.empty:
        mood_songs = songs[songs['mood'] == prediction]

    selected_story = mood_stories.sample(1).iloc[0]
    session['story_title']   = selected_story['story_title']
    session['story_content'] = selected_story['content']
    session['mood']          = prediction
    session['lang']          = selected_lang

    # Get fresh Spotify tracks (returns empty list if API keys match placeholders/fail)
    dynamic_songs = get_dynamic_songs(prediction, selected_lang, limit=8)

    # Combine local dataset with fresh Spotify data
    combined_songs = dynamic_songs + mood_songs.to_dict('records')
    
    song_list = enrich_songs(combined_songs)
    random.shuffle(song_list)
    top_song  = song_list[0]

    # Store the full list for later use
    session['song_list'] = song_list

    return render_template('choose.html', mood=prediction.capitalize())

@app.route('/show_story', methods=['POST'])
def show_story():
    # Use data stored in session
    return render_template('result.html',
                           mood=session.get('mood', '').capitalize(),
                           story_title=session.get('story_title', ''),
                           story_content=session.get('story_content', ''),
                           song_title='',
                           song_list=[],
                           selected_lang=session.get('lang', ''),
                           show_only='story')

@app.route('/show_songs', methods=['POST'])
def show_songs():
    # Retrieve the song list prepared earlier
    song_list = session.get('song_list', [])
    top_song = song_list[0] if song_list else {}
    return render_template('result.html',
                           mood=session.get('mood', '').capitalize(),
                           story_title=session.get('story_title', ''),
                           story_content=session.get('story_content', ''),
                           song_title=top_song.get('song_title', ''),
                           song_list=song_list,
                           selected_lang=session.get('lang', ''),
                           show_only='songs')

@app.route('/refresh_song', methods=['POST'])
def refresh_song():
    stories, songs = load_data()
    mood = session.get('mood', 'happy')
    lang = session.get('lang', 'english')
    story_title = session.get('story_title', '')
    story_content = session.get('story_content', '')

    mood_songs = songs[(songs['mood'] == mood) & (songs['language'] == lang)]
    if mood_songs.empty:
        mood_songs = songs[songs['mood'] == mood]

    # Get fresh Spotify tracks (returns empty list if API keys match placeholders/fail)
    dynamic_songs = get_dynamic_songs(mood, lang, limit=8)

    # Combine local dataset with fresh Spotify data
    combined_songs = dynamic_songs + mood_songs.to_dict('records')

    song_list = enrich_songs(combined_songs)
    random.shuffle(song_list)
    top_song = song_list[0]
    session['song_list'] = song_list

    return render_template('result.html',
                           mood=mood.capitalize(),
                           story_title=story_title,
                           story_content=story_content,
                           song_title=top_song['song_title'],
                           song_list=song_list,
                           selected_lang=lang,
                           show_only='songs')

if __name__ == '__main__':
    app.run(debug=True)
