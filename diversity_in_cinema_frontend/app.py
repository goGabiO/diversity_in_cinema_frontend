import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from diversity_in_cinema_frontend.api import *
import requests

CSS = """
h1 {
    color: black;
}
h2 {
    color: black;
}
h3 {
    color: black;
}
p {
    color: black;
}
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# @st.cache
# def load_image(path):
#     with open(path, 'rb') as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()
#     return encoded


# def image_tag(path):
#     encoded = load_image(path)
#     tag = f'<img src="data:faces/webp;base64,{encoded}">'
#     return tag


# def background_image_style(path):
#     encoded = load_image(path)
#     style = f'''
#     <style>
#     .stApp {{
#         background-image: url("data:faces/webp;base64,{encoded}");
#         background-size: cover;
#     }}
#     </style>
#     '''
#     return style


# image_path = 'faces.webp'
# image_link = '~/code/moe221/diversity_in_cinema_frontend/'

# st.write(background_image_style(image_path), unsafe_allow_html=True)

st.sidebar.header("Diversity and Representation in Hollywood")

option = st.sidebar.selectbox("Select a movie to view",
                                     ('','Man of Steel (2013)', 'Ace Ventura: Pet Detective (1994)'))

if option != "":
    select_status = st.sidebar.radio(
        "Pages", ('Info', 'Gender Statistics', 'Race Statistics',
                  'Statistical Overview'))
    st.title(f'{option}')
    if select_status == 'Info':
        col1, col2, col3 = st.columns(3)
        with col1:
            pass

        with col2:
            movie_info = fetch_movie_basic_data(option)
            movie_poster = movie_info[1]['poster_path']
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2{movie_poster}'
            response = requests.get(url.strip(), stream=True)
            image = Image.open(response.raw)
            st.image(image, use_column_width=True, output_format="JPG")

        with col3:
            pass

        col1, col2, col3 = st.columns(3)
        with col1:
            movie_basic = fetch_movie_basic_data(option)
            st.subheader("Relase Date")
            st.text(movie_basic[1]['release_date'])
            movie_info = fetch_movie_details(option)
            st.subheader("Genres")
            for index in range(len(movie_info['genres'])):
                st.text(movie_info['genres'][index]['name'])

        with col2:
            movie_info = fetch_movie_details(option)
            st.subheader("Languages")
            for index in range(len(movie_info['spoken_languages'])):
                st.text(movie_info['spoken_languages'][index]['english_name'])
            st.subheader('Revenue')
            revenue = movie_info['revenue']
            st.text(f'${revenue}')
            st.subheader('Runtime')
            runtime = movie_info['runtime']
            st.text(f'{runtime} minutes')

        with col3:
            movie_info = fetch_movie_credits(option)

    elif select_status == 'Gender Statistics':
        with st.container():
            st.header("Statistics")
            option_new = option.replace(':','')
            search_terms = option_new.lower().split()
            movie_name = '_'.join(search_terms)
            file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/gender_statistics.csv'
            df = pd.read_csv(file_name)
            x = df["gender"].value_counts().index
            y = df["gender"].value_counts().values
            fig, ax = plt.subplots()
            plt.bar(x, y)
            st.pyplot(fig)

    else:
        pass

else:
    st.title("Diversity and Representation in Hollywood")
    url = 'https://i.pinimg.com/originals/d8/9b/35/d89b3534d687eb456c47c4e5097b81c6.png'
    response = requests.get(url.strip(), stream=True)
    image = Image.open(response.raw)
    st.image(image, use_column_width=True, output_format="PNG")


# with st.container():
#     if option != "":
#         movie_info = fetch_movie_basic_data(option)
#         movie_poster = movie_info[1]['poster_path']
#         url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2{movie_poster}'
#         response = requests.get(url.strip(), stream=True)
#         image = Image.open(response.raw)
#         st.image(image, width=350, output_format="JPG")
