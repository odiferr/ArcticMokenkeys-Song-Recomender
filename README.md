"# ArcticMokenkeys-Song-Recomender" 

## ArcticMokenkeys-Song-Recomender

Welcome to the **Arctic Mokenkeys-Song-Recomender Song Recommendation System** This hybrid system combines **TF-IDF** and **Sentiment Analysis** to recommend songs that match your vibe. Whether you're a music lover or a data science enthusiast, this project is designed to bring the best of both worlds together.


## Why Arctic Monkeys?

As a huge **Arctic Monkeys*** fan, I knew they had written over 200 songs, but I always found myself sticking to the same ones. I wanted something more specific, a better way to discover new tracks that really match the vibe I’m looking for. That’s why I created this system! It’s designed to recommend songs based on **lyrics decriptions** and **sentiment**, so you get suggestions that truly align with their unique style. This project is a perfect mix of my love for their music and my passion for programming. By diving into their lyrics, the system curates personalized playlists that match the mood, tone, and lyrical vibe you’re after!


## **How It Works** 

The system uses two main techniques to recommend songs:

1. **TF-IDF & Cosine Similarity**:
   - Computes a **TF-IDF matrix** for song lyrics.
   - Calculates **cosine similarity** between the user input and each song.
   - Recommends songs with the highest similarity to the user input.

2. **Sentiment Analysis**:
   - Uses **NLTK's VADER Sentiment Analyzer** to analyze the emotional tone of the user input and song lyrics.
   - Recommends songs with similar sentiment to the user’s input.

The **hybrid approach** combines both techniques using a weighted average of the TF-IDF and sentiment scores to deliver the best recommendations.


## **Features** 

- **Preprocessing**: Tokenizes, removes stopwords, and lemmatizes user input and song lyrics for better analysis.
- **Database Interaction**: Fetches song titles and lyrics from an **SQLite database**.
- **Sentiment-Aware**: Analyzes the emotional tone of user input and song lyrics to provide mood-based recommendations.
- **Hybrid Recommendation**: Combines TF-IDF and sentiment analysis for the most relevant song suggestions.

---

##  **Requirements** 

To run this project, you'll need the following Python libraries:

- `sqlite3`: For database interactions.
- `numpy`: For numerical operations.
- `sklearn`: For TF-IDF vectorization and cosine similarity calculations.
- `nltk`: For text preprocessing, tokenization, stopword removal, lemmatization, and sentiment analysis.
- `flask`: For serving the app over HTTP.

---

##  **Installation** 

1) **Clone the repository** : git clone https://github.com/your-username/ArcticMonkeys-Song-Recommender.git

2) **Navigate to the project directory**: cd ArcticMonkeys-Song-Recommender

3) **Install the required libraries**: pip install nltk sklearn numpy flask

4) **Download NLTK data (if not already downloaded)**:
   
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('vader_lexicon')
  Install the required libraries:




**Running the System**

Start the Flask server:

Open your browser and navigate to: http://127.0.0.1:5000/
Enter your input (e.g., a line of lyrics or a mood) and let the system recommend songs!

**Project Structure**
├── app.py                    # Flask application
├── arctic_monkeys_lyrics.db  # SQLite database containing Arctic Monkeys lyrics
├── static/styles             # Static files (Contains the CSS file)
├── templates/index.html      # HTML templates for rendering pages
├── Main.py                   # Main logic for song recommendation system
├── requirements.txt          # List of dependencies
└── README.md                 # Project documentation
 
 **Contributing**
Contributions are welcome! I’m a big believer in Kaizen—the philosophy of making small, continuous improvements. If you have any ideas for bettering this project or adding new features, I’d love to hear them! Feel free to open an issue or submit a pull request anytime




