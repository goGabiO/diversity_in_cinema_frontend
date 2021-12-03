import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from diversity_in_cinema_frontend.api import *
from diversity_in_cinema_frontend.visualizations import *
from diversity_in_cinema_frontend.utils import *
import requests

movie_options = get_movie_list("CSVs")

option = st.sidebar.selectbox("Select a movie to view", (movie_options))


if option == "":
    select_status = st.sidebar.radio("Pages", ('Home', 'Overall Statistics'))
    CSS = """
    h1 {
        color: black;
        font-family: "Lucida Console", "Courier New", monospace;
     }
    h2 {
        color: black;
        font-family: "Lucida Console", "Courier New", monospace;
     }
    h3 {
        color: black;
        font-family: "Lucida Console", "Courier New", monospace;
     }
    p {
        color: black;
        font-family: "Lucida Console", "Courier New", monospace;
     }
     body {background-color: white;}
     """
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

    if select_status == 'Home':

        st.title("Diversity in")

        image = Image.open('Hollywood-Sign.png')
        st.image(image, use_column_width=True)

        st.text('')
        st.text('Diversity in Hollywood uses deep learning to detect faces in')
        st.text('every key frame of a selected movie and generates a dashboard showing statistics')
        st.text('on gender and race representation, along with a composite "face of the movie"')

    elif select_status == 'Overall Statistics':

        col1, col2, col3 = st.columns([6,6,1])

        with col1:
            total_stats_df = pd.read_csv('overall_dash_data.csv')
            go_fig = women_revenue_scatter(total_stats_df)
            st.plotly_chart(go_fig, use_column_width=True)

        with col1:
            st.write("")
            go_fig_2 = plot_gender_timeline(total_stats_df, "bar")
            st.plotly_chart(go_fig_2, use_column_width=True)


        with col1:
            st.write("---"*500)
            go_fig_3 = plot_race_timeline(total_stats_df)
            st.plotly_chart(go_fig_3, use_column_width=False)

        with col1:
            go_fig_4 = poc_scatter_revenue(total_stats_df)
            st.plotly_chart(go_fig_4, use_column_width=False)


    # @st.cache
    # def load_image(path):
    #     with open(path, 'rb') as f:
    #         data = f.read()
    #     encoded = base64.b64encode(data).decode()
    #     return encoded

    # def image_tag(path):
    #     encoded = load_image(path)
    #     tag = f'<img src="data:wp7062810/jpg;base64,{encoded}">'
    #     return tag

    # def background_image_style(path):
    #     encoded = load_image(path)
    #     style = f'''
    #     <style>
    #     .stApp {{
    #         background-image: url("data:wp7062810/jpg;base64,{encoded}");
    #         background-size: cover;
    #     }}
    #     </style>
    #     '''
    #     return style

    # image_path = 'wp7062810.jpg'
    # image_link = '~/code/moe221/diversity_in_cinema_frontend/'

    # st.write(background_image_style(image_path), unsafe_allow_html=True)

    # with col1:
    #     url = 'https://i.pinimg.com/originals/d8/9b/35/d89b3534d687eb456c47c4e5097b81c6.png'
    #     response = requests.get(url.strip(), stream=True)
    #     image = Image.open(response.raw)
    #     st.image(image, use_column_width=True, output_format="PNG")


else:
    st.sidebar.header("Diversity in Hollywood")
    select_status = st.sidebar.radio(
        "Pages", ('Info', 'Gender Statistics', 'Race Statistics'))
    # 'Statistical Overview'
    st.title(f'{option}')
    if select_status == 'Info':

        col1, col2, col3 = st.columns(3)
        with col1:
            st.text('')
            st.text('')
            st.text('')
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

        col1, col2, col3, col4 = st.columns([5,1,1,1])

        #option_new = option.replace(':','').replace(',',' ')
        search_terms = option.split()
        movie_name = '_'.join(search_terms)
        file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/statistics'
        df = pd.read_csv(file_name)

        with col1:
            st.header("Gender Statistics")

            go_fig = run_time(movie_name)
            st.plotly_chart(go_fig, use_column_width=True)

        with col1:
            go_fig = man_woman_screentime_bar(df)
            st.plotly_chart(go_fig, use_column_width=True)

        with col1:

            go_fig = only_women_screentime_donut(df)
            st.plotly_chart(go_fig, use_column_width=True)

    elif select_status == 'Race Statistics':

        col1, col2, col3, col4 = st.columns([5,1,1,1])

        #option_new = option.replace(':','').replace(',',' ')
        search_terms = option.split()
        movie_name = '_'.join(search_terms)
        file_name = f'https://storage.googleapis.com/wagon-data-735-movie-diversity/CSVs/{movie_name}/statistics'
        df = pd.read_csv(file_name)

        with col1:
            st.header("Race Statistics")

            go_fig = run_time(movie_name, by="race")
            st.plotly_chart(go_fig, use_column_width=True)

        with col1:
            go_fig = r_screentime_donut(df)
            st.plotly_chart(go_fig, use_column_width=True)

        with col1:

            go_fig = woc_screentime_donut(df)
            st.plotly_chart(go_fig, use_column_width=True)


    else:
        pass
