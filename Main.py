import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("vader_lexicon")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer


# Database Setup
DATABASE_NAME = "arctic_monkeys_lyrics.db"


def preprocess_text(text):
    """Preprocess text by tokenizing, removing stopwords, and lemmatizing."""
    # Tokenize text into words
    tokens = word_tokenize(text.lower())

    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return lemmatized_tokens


def fetch_songs_from_db():
    """Fetch all songs from the database."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, lyrics FROM songs")
        songs = cursor.fetchall()
        #conn.close()
    return songs


def recommend_songs_tfidf(user_input, songs):
    """Recommend songs using TF-IDF and cosine similarity."""
    # Preprocess user input
    user_keywords = " ".join(preprocess_text(user_input))

    # Extract lyrics from songs
    song_titles = [title for title, _ in songs]
    song_lyrics = [lyrics for _, lyrics in songs]

    # Compute TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(song_lyrics)

    # Transform user input into TF-IDF vector
    user_tfidf = vectorizer.transform([user_keywords])

    # Compute cosine similarity between user input and song lyrics
    similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

    # Pair song titles with similarity scores
    scored_songs = list(zip(song_titles, similarity_scores))

    # Sort songs by similarity score (descending)
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Return top recommendations
    return scored_songs


def analyze_sentiment(text):
    """Analyze sentiment using NLTK's VADER."""
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)["compound"]  # Compound score ranges from -1 (negative) to 1 (positive)


def recommend_songs_sentiment(user_input, songs):
    """Recommend songs based on sentiment analysis."""
    # Analyze sentiment of user input
    user_sentiment = analyze_sentiment(user_input)

    # Score songs based on sentiment similarity
    scored_songs = []
    for title, lyrics in songs:
        song_sentiment = analyze_sentiment(lyrics)
        sentiment_diff = abs(user_sentiment - song_sentiment)
        scored_songs.append((title, sentiment_diff))

    # Sort songs by sentiment difference (ascending)
    scored_songs.sort(key=lambda x: x[1])

    # Return top recommendations
    return scored_songs


def recommend_songs_hybrid(user_input, songs):
    """Hybrid recommendation system combining TF-IDF and sentiment analysis."""
    # Step 1: Score songs using TF-IDF
    tfidf_recommendations = recommend_songs_tfidf(user_input, songs)

    # Step 2: Score songs using sentiment analysis
    sentiment_recommendations = recommend_songs_sentiment(user_input, songs)

    # Step 3: Combine scores (e.g., weighted average)
    combined_scores = {}
    for title, score in tfidf_recommendations:
        combined_scores[title] = combined_scores.get(title, 0) + score * 0.6  # Weight for TF-IDF
    for title, score in sentiment_recommendations:
        combined_scores[title] = combined_scores.get(title, 0) + (1 - score) * 0.4  # Weight for sentiment

    # Sort songs by combined score (descending)
    scored_songs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top recommendations
    return scored_songs[:2]


def main():
    # Get user input
    user_input = input("Describe the type of song you want: ")

    # Fetch songs from the database
    songs = fetch_songs_from_db()

    # Get recommendations
    recommendations = recommend_songs_hybrid(user_input, songs)

    if not recommendations:
        print("No songs found matching your description. Try again!")
    else:
        print("\n🎵 Recommended Songs:")
        for i, (title) in enumerate(recommendations, start=1):
            print(f"{i}. {title} ")


if __name__ == "__main__":
    main()