import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2beeb6fbfa8d03e911439eb4d6e6ff25"
    
    data = requests.get(url).json()
    
    if 'poster_path' in data and data['poster_path'] is not None:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

imageCarouselComponent(imageUrls=imageUrls, height=200)

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommended_movies = []
    recommended_posters = []
    
    for i in distances[1:6]:  # Get top 5 similar movies
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Show recommendations when button is clicked
if st.button("Show Recommend"):
    recommended_names, recommended_posters = recommend(selectvalue)
    
    # Display the recommended movies and their posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_names[0])
        st.image(recommended_posters[0])
    
    with col2:
        st.text(recommended_names[1])
        st.image(recommended_posters[1])
    
    with col3:
        st.text(recommended_names[2])
        st.image(recommended_posters[2])
    
    with col4:
        st.text(recommended_names[3])
        st.image(recommended_posters[3])
    
    with col5:
        st.text(recommended_names[4])
        st.image(recommended_posters[4])
