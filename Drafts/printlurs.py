import lyricsgenius


# Use a valid Genius API token (replace with your real one)
ACCESS_TOKEN = "44RXXcUhdzY2MOvgdVoC_9oGkdWl-Y7R-2tzSAaMHyq0a535pz1kYEPH9b9yZGZJ"

# Initialize Genius API
genius = lyricsgenius.Genius(ACCESS_TOKEN)

# Search for the artist
artist = genius.search_artist("El Alfa", max_songs=1, sort="title")

# Check if the artist was found

        # with open('lyrics.txt', 'w', encoding='utf-8') as f:
        #     f.write(song.lyrics)
        # print("Lyrics saved successfully!")
       # Retrieve the song


# Check if the artist was found
if artist:
    song = artist.song("4k")  # Retrieve the song

    if song:  # Check if the song was found
        print(song.lyrics)  # Print lyrics to the console
    else:
        print("Song not found!")
else:
    print("Artist not found!")