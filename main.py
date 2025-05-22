import streamlit as st
from auth import show_login
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import urllib.parse

# API keys
YOUTUBE_API_KEY = "AIzaSyA7gwKRhtXqQ0XiiiRMiGKrJ_MYHfyJU2g"
GOOGLE_API_KEY = "AIzaSyBl98akzD4WVHlxIFTioRIQ_YeUBkNKX18"
GOOGLE_CX = "b1730c6eab6484013"

# Dataset paths
movies_path = r"D:\\Movie\\tmdb_5000_movies.csv"
credits_path = r"D:\\Movie\\tmdb_5000_credits.csv"

# Session check and login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    show_login()
    st.stop()

# Load data
@st.cache_data
def load_data():
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)
    movies.rename(columns={'id': 'movie_id'}, inplace=True)
    data = movies.merge(credits, on='movie_id')
    data.rename(columns={'title_x': 'title'} if 'title_x' in data.columns else {'title_y': 'title'}, inplace=True)
    data['overview'] = data['overview'].fillna('')
    return data

# Create similarity matrix
@st.cache_resource
def create_similarity(data):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['overview'])
    similarity = cosine_similarity(tfidf_matrix)
    return similarity

# Recommend movies
def recommend(title, data, similarity):
    if title not in data['title'].values:
        return []
    idx = data[data['title'] == title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    return [{
        "title": data.iloc[i]['title'],
        "overview": data.iloc[i]['overview']
    } for i, _ in scores]

# Get trending movies
def get_trending(data, n=5):
    trending = data[data['vote_count'] > 1000]
    trending = trending.sort_values(by=['vote_average', 'vote_count'], ascending=False)
    return trending[['title', 'overview', 'vote_average', 'popularity']].head(n).to_dict(orient='records')

# Fetch poster
def fetch_movie_poster(title):
    query = urllib.parse.quote(f"{title} movie poster")
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&searchType=image"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if "items" in results:
            return results["items"][0]["link"]
    return "Poster not found"

# Fetch trailer
def fetch_trailer_from_movie_name(movie_name):
    encoded_name = urllib.parse.quote(f"{movie_name} trailer")
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={encoded_name}&key={YOUTUBE_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            video_id = data["items"][0]["id"].get("videoId")
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
    return "Trailer not found"

# Home Page
def home_page():
    st.markdown("""
        <style>.center {text-align: center;}</style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="center">
        <h3>Your personal assistant for discovering trending and similar movies.</h3>
        <p>Select options from the sidebar to get started:</p>
        <ul>
            <li><strong>Recommend:</strong> Get movies similar to the one you like.</li>
            <li><strong>Trending:</strong> See popular and top-rated movies.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"Logged in as: {st.session_state.get('username', 'Guest')}")

# Main App
st.set_page_config(page_title="Movie Recommendation System")

# Sidebar with Logout button
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Recommend", "Trending"])

# Logout button
if st.session_state.get("logged_in", False):
    if st.sidebar.button("Logout"):
        for key in ["logged_in", "username"]:
            st.session_state.pop(key, None)
        st.success("You have been logged out.")
        st.stop()

# Load data and similarity
data = load_data()
similarity = create_similarity(data)

# Pages
if menu == "Home":
    home_page()

elif menu == "Recommend":
    movie_list = data['title'].drop_duplicates().sort_values().tolist()
    selected_movie = st.selectbox("Select a movie to get recommendations", movie_list)

    if st.button("Show Recommendations"):
        recommendations = recommend(selected_movie, data, similarity)
        if not recommendations:
            st.error("Movie not found.")
        else:
            st.subheader("Top 5 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}. {rec['title']}**")
                trailer_link = fetch_trailer_from_movie_name(rec['title'])
                poster_link = fetch_movie_poster(rec['title'])
                if poster_link == "Poster not found":
                    st.error("Poster not found for this movie.")
                else:
                    st.image(poster_link, width=200, caption="Movie Poster")
                with st.expander("Show Overview"):
                    st.write(rec['overview'])
                st.markdown(f"[\U0001F3A5 Watch Trailer]({trailer_link})")
                st.markdown("---")

elif menu == "Trending":
    st.subheader("\U0001F525 Trending Movies")
    trending_movies = get_trending(data)
    for i, movie in enumerate(trending_movies, 1):
        with st.expander(f"{i}. {movie['title']}"):
            st.markdown(f"**Rating:** {movie['vote_average']}")
            st.markdown(f"**Popularity:** {movie['popularity']}")
            st.markdown("**Overview:**")
            st.write(movie['overview'])
            poster_link = fetch_movie_poster(movie['title'])
            if poster_link == "Poster not found":
                st.error("Poster not found for this movie.")
            else:
                st.image(poster_link, width=200, caption="Movie Poster")
            trailer_link = fetch_trailer_from_movie_name(movie['title'])
            st.markdown(f"[\U0001F3A5 Watch Trailer]({trailer_link})")
