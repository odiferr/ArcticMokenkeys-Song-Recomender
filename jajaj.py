import requests
import sqlite3
import time
from bs4 import BeautifulSoup

# Genius API Setup
GENIUS_ACCESS_TOKEN = "44RXXcUhdzY2MOvgdVoC_9oGkdWl-Y7R-2tzSAaMHyq0a535pz1kYEPH9b9yZGZJ"
GENIUS_API_URL = "https://api.genius.com"
ARTIST_NAME = "Arctic Monkeys"
DATABASE_NAME = "arctic_monkeys_lyrics.db"


# Database Setup
def create_database():
    """Create a SQLite database to store song lyrics."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            lyrics TEXT NOT NULL,
            artist TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_song_to_db(title, lyrics, artist):
    """Save a song's title and lyrics to the database, avoiding duplicates."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Check if the song is already in the database
    cursor.execute("SELECT title FROM songs WHERE title = ?", (title,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO songs (title, lyrics, artist) VALUES (?, ?, ?)", (title, lyrics, artist))
        conn.commit()

    conn.close()


def search_songs_by_artist(artist_name, page=1):
    """Search for songs by the artist using Genius API (Paginated)."""
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": artist_name, "page": page}
    response = requests.get(f"{GENIUS_API_URL}/search", headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching song data:", response.json())
        return []

    return response.json().get("response", {}).get("hits", [])


def get_song_lyrics(song_url):
    """Fetch song lyrics from the Genius webpage."""
    response = requests.get(song_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find lyrics in the updated HTML structure
        lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
        if lyrics_divs:
            lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
            return lyrics

    return None


def main():
    create_database()
    print(f"Fetching songs by {ARTIST_NAME} from Genius...")

    page = 1
    while True:
        songs = search_songs_by_artist(ARTIST_NAME, page)
        if not songs:
            break  # Stop when no more songs are found

        for hit in songs:
            song = hit["result"]
            song_title = song["title"]
            song_url = song["url"]
            artist = song["primary_artist"]["name"]

            if ARTIST_NAME.lower() in artist.lower():
                print(f"Fetching lyrics for: {song_title}...")
                lyrics = get_song_lyrics(song_url)
                if lyrics:
                    save_song_to_db(song_title, lyrics, artist)
                    print(f"✅ Saved lyrics for: {song_title}")
                else:
                    print(f"❌ Could not retrieve lyrics for: {song_title}")

            time.sleep(1)  # Avoid rate-limiting

        page += 1  # Move to the next page

    print("\n🎵 All songs and lyrics stored in database!")


if __name__ == "__main__":
    main()