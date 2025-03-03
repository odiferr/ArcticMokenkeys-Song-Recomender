from flask import Flask, render_template, request , flash
import sqlite3
from Main import recommend_songs_hybrid, fetch_songs_from_db  # Replace with your actual module name

app = Flask(__name__)
app.secret_key = 'DDrummer750'  # Necessary for flash messages

# Database Setup
DATABASE_NAME = "arctic_monkeys_lyrics.db"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Collect input data from the form
            user_input = request.form['user_input']

            # Fetch songs from the database
            songs = fetch_songs_from_db()

            # Get recommendations
            recommendations = recommend_songs_hybrid(user_input, songs)

            if not recommendations:
                flash("No songs found matching your description. Try again!", "warning")
            else:
                # Pass recommendations to the templates
                return render_template('index.html', recommendations=recommendations)

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            # return redirect(url_for('home'))

    # Render the form for GET requests
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)