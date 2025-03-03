import sqlite3
import nltk
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



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
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, lyrics FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return songs


def recommend_songs(user_input):
    """Recommend songs based on user input."""
    # Step 1: Preprocess user input
    user_keywords = preprocess_text(user_input)
    print(f"Extracted Keywords: {user_keywords}")

    # Step 2: Fetch all songs from the database
    songs = fetch_songs_from_db()

    # Step 3: Score songs based on keyword matches
    scored_songs = []
    for title, lyrics in songs:
        lyrics_keywords = preprocess_text(lyrics)
        match_score = sum(keyword in lyrics_keywords for keyword in user_keywords)
        if match_score > 0:
            scored_songs.append((title, match_score))

    # Step 4: Sort songs by match score (descending)
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Step 5: Return top recommendations
    return scored_songs[:5]  # Return top 5 songs


def main():
    # Get user input
    user_input = input("Describe the type of song you want: ")

    # Get recommendations
    recommendations = recommend_songs(user_input)

    if not recommendations:
        print("No songs found matching your description. Try again!")
    else:
        print("\n🎵 Recommended Songs:")
        for i, (title, score) in enumerate(recommendations, start=1):
            print(f"{i}. {title} (Match Score: {score})")


if __name__ == "__main__":
    main()