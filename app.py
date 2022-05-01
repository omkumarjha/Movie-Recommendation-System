import streamlit as st
import pickle
import pandas as pd
import requests    # This Build in module mainly Used for hitting the API

# Getting the content from the pickel 
movies_dict = pickle.load(open("temp.txt","rb"))   # Load function open file mai se content ko read karta hai
data = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.txt","rb"))


# Showing The heading
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(      # selected_movie_name variable us movie ke name contain karega jisko user ne select box mai enter kiya hai
'How would you like to be contacted?',
data["title"].values)

# Recommend function
def recommend(movie):

    movie_index = data[data["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x : x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []


    for i in movies_list:
        recommended_movies_poster.append(fetch_poster(data.iloc[i[0]].id))
        recommended_movies.append(data.iloc[i[0]].title)

    return recommended_movies , recommended_movies_poster

# function to get poster of the movie with the help of it's id

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=56909e3c0d75297a82f4bb4dafbf6a8e&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data["poster_path"]


if st.button('Recommend'):
    recommended_movies , recommended_movies_poster = recommend(selected_movie_name)
     
    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
         st.text(recommended_movies[0])
         st.image(recommended_movies_poster[0])

    with col2:
         st.text(recommended_movies[1])
         st.image(recommended_movies_poster[1])

    with col3:
         st.text(recommended_movies[2])
         st.image(recommended_movies_poster[2])

    with col4:
         st.text(recommended_movies[3])
         st.image(recommended_movies_poster[3])

    with col5:
         st.text(recommended_movies[4])
         st.image(recommended_movies_poster[4])


# Command is 'streamlit run app.py'