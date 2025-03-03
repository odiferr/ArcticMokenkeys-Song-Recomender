import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Genius API Setup
GENIUS_ACCESS_TOKEN = "44RXXcUhdzY2MOvgdVoC_9oGkdWl-Y7R-2tzSAaMHyq0a535pz1kYEPH9b9yZGZJ"  # Replace with your Genius API Key
GENIUS_SEARCH_URL = "https://api.genius.com/search"

# Download NLTK data (only needed once)
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger", force=True)

def get_song_recommendation(user_input):
    """Process user input and fetch song recommendations from Genius API."""

    # Validate user input
    if not user_input or not user_input.strip():
        return {"error": "Please provide a valid description of the song you want."}

    # Tokenize and extract keywords using NLTK
    tokens = word_tokenize(user_input.strip())
    tagged_tokens = pos_tag(tokens)

    # Extract nouns, adjectives, verbs, and adverbs
    keywords = [word for word, pos in tagged_tokens if pos.startswith(("NN", "JJ", "VB", "RB"))]
    query = " ".join(keywords)

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

        # Get the top 5 search results
        recommendations = []
        for i, hit in enumerate(results[:5]):  # Limit to 5 songs
            song = hit["result"]
            song_title = song["title"]
            artist = song["primary_artist"]["name"]
            song_url = song["url"]
            recommendations.append({
                "rank": i + 1,
                "song_title": song_title,
                "artist": artist,
                "song_url": song_url,
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