import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from bs4 import BeautifulSoup

# Genius API Setup
GENIUS_ACCESS_TOKEN = "44RXXcUhdzY2MOvgdVoC_9oGkdWl-Y7R-2tzSAaMHyq0a535pz1kYEPH9b9yZGZJ"  # Replace with your Genius API Key
GENIUS_SEARCH_URL = "https://api.genius.com/search"

# Download NLTK data (only needed once)
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger", force=True)
# nltk.download("wordnet")

def get_synonyms(word):
    """Get synonyms for a word using WordNet."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def extract_keywords(user_input):
    """Extract and expand keywords from user input."""
    tokens = word_tokenize(user_input.strip())
    tagged_tokens = pos_tag(tokens)
    keywords = [word for word, pos in tagged_tokens if pos.startswith(("NN", "JJ", "VB", "RB")) and word.lower() not in nltk.corpus.stopwords.words("english")]
    expanded_keywords = keywords + [syn for word in keywords for syn in get_synonyms(word)]
    return " ".join(expanded_keywords)

def get_album_art(song_url):
    """Fetch album art URL from the song page."""
    response = requests.get(song_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        album_art = soup.find("img", {"class": "cover_art-image"})
        if album_art:
            return album_art["src"]
    return None

def filter_by_artist(results, artist="Arctic Monkeys"):
    """Filter results by artist."""
    filtered_results = []
    for hit in results:
        song = hit["result"]
        if "primary_artist" in song and artist.lower() in song["primary_artist"]["name"].lower():
            filtered_results.append(hit)
    return filtered_results

def get_song_recommendation(user_input, artist="Arctic Monkeys"):
    """Process user input and fetch song recommendations from Genius API."""

    # Validate user input
    if not user_input or not user_input.strip():
        return {"error": "Please provide a valid description of the song you want."}

    # Extract and expand keywords
    query = extract_keywords(user_input)
    if not query:
        return {"error": "Couldn't understand your request. Try describing the song differently!"}

    # Search Genius API
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": query}

    try:
        response = requests.get(GENIUS_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")  # Print the raw response content

        # Check if the response content is valid JSON
        if not response.text.strip():
            return {"error": "Empty response from Genius API."}

        try:
            data = response.json()
        except ValueError as e:
            return {"error": f"Invalid JSON response: {e}"}

        results = data.get("response", {}).get("hits", [])

        if not results:
            return {"error": "No songs found matching your description. Try again!"}

        # Filter results by artist
        results = filter_by_artist(results, artist)

        if not results:
            return {"error": "No Arctic Monkeys songs found matching your description. Try again!"}

        # Get the top 5 search results
        recommendations = []
        for i, hit in enumerate(results[:5]):  # Limit to 5 songs
            song = hit["result"]
            song_title = song["title"]
            artist = song["primary_artist"]["name"]
            song_url = song["url"]
            album_art = get_album_art(song_url)
            recommendations.append({
                "rank": i + 1,
                "song_title": song_title,
                "artist": artist,
                "song_url": song_url,
                "album_art": album_art,
            })

        return recommendations
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching song data: {e}"}

# Example Usage
if __name__ == "__main__":
    user_query = input("Describe the type of song you want: ")
    recommendations = get_song_recommendation(user_query)

    if "error" in recommendations:
        print(recommendations["error"])
    else:
        print("🎵 Recommended Songs:")
        for song in recommendations:
            print(f"{song['rank']}. **{song['song_title']}** by **{song['artist']}**")
            print(f"   Listen here: {song['song_url']}")
            if song["album_art"]:
                print(f"   Album Art: {song['album_art']}")