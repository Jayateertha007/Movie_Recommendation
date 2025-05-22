Welcome to the Movie Recommendation System, an interactive web app built with Streamlit that suggests movies based on your selected favorite. It integrates The Movie Database (TMDB) via RapidAPI to dynamically fetch movie details, posters, genres, and more.

🚀 Features
🔍 Personalized Recommendations: Choose any movie to get top 5 similar suggestions based on content similarity.

🖼️ Movie Posters & Details: View posters, release dates, genres, and overviews fetched live from TMDB.

📈 Trending Movies Section: See the top trending movies calculated using popularity and vote scores.

⚡ Fast and Interactive UI: Powered by Streamlit for seamless user interaction and fast performance.

🛠️ Tech Stack
Frontend/UI: Streamlit

Backend: Python

Data Source: TMDB Alternative API on RapidAPI

ML Model: Content-based filtering using cosine similarity (precomputed)

📦 Data
Movie metadata and similarity scores are preprocessed and stored in movies_with_ids.pkl and similarity.pkl.

TMDB IDs are used to dynamically fetch live data such as posters and overviews.

📁 Project Structure
bash
Copy
Edit
├── app.py                         # Main Streamlit application
├── data/
│   └── movies_with_ids.pkl       # Preprocessed movie data with TMDB IDs
├── similarity.pkl                # Precomputed cosine similarity matrix
🔐 Note
This app uses a RapidAPI key to access TMDB data. To run the app locally:

Replace the placeholder API key with your own from RapidAPI.

Install dependencies with pip install -r requirements.txt.

Run the app using streamlit run app.py.
