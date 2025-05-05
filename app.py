import streamlit as st
import pickle
import requests
import time
import gzip

movies = pickle.load(open('movie_list.pkl', 'rb'))
with gzip.open("similarity_compressed.pkl.gz","rb") as f:
    similarity=pickle.load(f)

# function to Fetch movie details
def fetch_movie_details(movie_id):
    api_key = "4d829fb0381ababdeb5b1fa55abaaba3" 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    
    poster_path = data.get('poster_path', '')
    poster = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
    overview = data.get('overview', 'No overview available.')
    rating = data.get('vote_average', 'N/A')
    
    return poster, overview, rating

# function for Recommending movies
def recommend(movie, num_recommendations=5):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_data = []
    for i in distances[1:num_recommendations+1]:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, overview, rating = fetch_movie_details(movie_id)
        recommended_data.append({
            'title': title,
            'poster': poster,
            'overview': overview,
            'rating': rating
        })

    return recommended_data

# Streamlit App - it will run in browser
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        color: white;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        border-radius: 8px;
    }
    img {
        border-radius: 10px;
        transition: transform .2s;
    }
    img:hover {
        transform: scale(1.05);
    }
    .movie-card {
        padding: 10px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #00FFFF;
        text-align: center;
        font-size: 14px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('🎥 Ultimate Movie Recommender')

selected_movie_name = st.selectbox(
    'Type or select a movie:',
    movies['title'].values
)

num_recommendations = st.slider(
    'How many recommendations you want?', 
    min_value=1, max_value=10, value=5
)

if st.button('Recommend Movies'):
    with st.spinner('Hold on... Generating your recommendations!'):
        time.sleep(1.5)
        recommended_movies = recommend(selected_movie_name, num_recommendations)

    st.markdown("<h3 style='text-align: center; color: #00FFFF;'>Your Recommendations</h3>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, movie in enumerate(recommended_movies):
        with cols[idx % 5]:
            st.image(movie['poster'], use_container_width=True)
            st.markdown(f"{movie['title']}")
            st.markdown(f"⭐ Rating: {movie['rating']}")
            with st.expander("See Overview"):
                st.write(movie['overview'])
            st.markdown("---")

# Footer part
st.markdown(
    """
    <div class="footer">
        Made by Dhruv Sharma
    </div>
    """,
    unsafe_allow_html=True
)


