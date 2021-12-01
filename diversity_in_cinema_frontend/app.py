import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from diversity_in_cinema_frontend.api import *
from diversity_in_cinema_frontend.visualizations import *
from diversity_in_cinema_frontend.utils import *
import requests

# CSS = """
# h1 {
#     color: black;
# }
# h2 {
#     color: black;
# }
# h3 {
#     color: black;
# }
# p {
#     color: black;
# }
# """
# st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

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

movie_options = get_movie_list("CSVs")

option = st.sidebar.selectbox("Select a movie to view", (movie_options))

if option != "":
    select_status = st.sidebar.radio(
        "Pages", ('Info', 'Gender Statistics', 'Race Statistics',
                  'Statistical Overview'))
    st.title(f'{option}')
    if select_status == 'Info':

        col1, col2, col3 = st.columns(3)
        with col1:
            movie_info = fetch_movie_basic_data(option)
            movie_poster = movie_info[1]['poster_path']
            url = f'https://www.themoviedb.org/t/p/w600_and_h900_bestv2{movie_poster}'
            response = requests.get(url.strip(), stream=True)
            image = Image.open(response.raw)
            st.image(image, use_column_width=True, output_format="JPG")

        with col2:
            url = 'https://www.freepnglogos.com/uploads/line-png/straight-vertical-line-transparent-27.png'
            response = requests.get(url.strip(), stream=True)
            image = Image.open(response.raw)
            st.image(image, use_column_width=True, output_format="PNG")

        with col3:
            # movie_face = option
            # url = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_face}.jpg'
            # response = requests.get(url.strip(), stream=True)
            # image = Image.open(response.raw)
            # st.image(image, use_column_width=True, output_format="JPG")
            pass

        col1, col2, col3 = st.columns(3)
        with col1:
            movie_basic = fetch_movie_basic_data(option)
            st.subheader("Relase Date")
            st.text(movie_basic[1]['release_date'])
            movie_info = fetch_movie_details(option)
            st.subheader('Runtime')
            runtime = movie_info['runtime']
            st.text(f'{runtime} minutes')

        with col2:
            movie_info = fetch_movie_details(option)
            st.subheader("Languages")
            for index in range(len(movie_info['spoken_languages'])):
                st.text(movie_info['spoken_languages'][index]['english_name'])
            st.subheader('Revenue')
            revenue = movie_info['revenue']
            st.text(f'${revenue}')

        with col3:
            movie_info = fetch_movie_details(option)
            st.subheader("Genres")
            for index in range(len(movie_info['genres'])):
                st.text(movie_info['genres'][index]['name'])

        st.header("Cast & Crew")

        col1, col2 = st.columns(2)

        with col1:
            movie_info = fetch_movie_credits(option)
            st.subheader("Cast")
            for index in range(len(movie_info['cast'])):
                if movie_info['cast'][index]['gender'] == 1:
                    name = movie_info['cast'][index]['name']
                    gender = 'Female'
                    st.text(f'{name}, {gender}')
                else:
                    name = movie_info['cast'][index]['name']
                    gender = 'Male'
                    st.text(f'{name}, {gender}')

        with col2:
            movie_info = fetch_movie_credits(option)
            st.subheader("Crew")
            for index in range(len(movie_info['crew'])):
                if movie_info['crew'][index]['gender'] == 1:
                    name = movie_info['crew'][index]['name']
                    gender = "Female"
                    job = movie_info['crew'][index]['job']
                    st.text(f'{name}, {gender}: {job}')
                else:
                    name = movie_info['crew'][index]['name']
                    gender = "Male"
                    job = movie_info['crew'][index]['job']
                    st.text(f'{name}, {gender}: {job}')



    elif select_status == 'Gender Statistics':
        with st.container():
            st.header("Gender Statistics")
            option_new = option.replace(':','')
            search_terms = option_new.lower().split()
            movie_name = '_'.join(search_terms)
            file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/statistics'
            df = pd.read_csv(file_name)

            go_fig = g_screentime_donut(df)
            st.plotly_chart(go_fig, use_container_width=True)

            go_2_fig = only_men_screentime_donut(df)
            st.plotly_chart(go_2_fig, use_container_width=True)

            go_3_fig = only_women_screentime_donut(df)
            st.plotly_chart(go_3_fig, use_container_width=True)

    elif select_status == 'Race Statistics':
        with st.container():
            st.header("Race Statistics")
            option_new = option.replace(':', '')
            search_terms = option_new.lower().split()
            movie_name = '_'.join(search_terms)
            file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/statistics'
            df = pd.read_csv(file_name)

            go_fig = r_screentime_donut(df)
            st.plotly_chart(go_fig, use_container_width=True)

            go_2_fig = woc_screentime_donut(df)
            st.plotly_chart(go_2_fig, use_container_width=True)


    else:
        pass

else:
    st.title("Diversity and Representation in Hollywood")
    url = 'https://i.pinimg.com/originals/d8/9b/35/d89b3534d687eb456c47c4e5097b81c6.png'
    response = requests.get(url.strip(), stream=True)
    image = Image.open(response.raw)
    st.image(image, use_column_width=True, output_format="PNG")
