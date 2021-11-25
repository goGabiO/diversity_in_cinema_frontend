import streamlit as st
import base64
import pandas as pd

CSS = """
h1 {
    color: white;
}
h2 {
    color: white;
}
h3 {
    color: white;
}
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded


def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:il_fullxfull.31046271/webp;base64,{encoded}">'
    return tag


def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:il_fullxfull.31046271/webp;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style


image_path = 'il_fullxfull.31046271.webp'
image_link = '~/code/moe221/diversity_in_cinema_frontend/'

st.write(background_image_style(image_path), unsafe_allow_html=True)
'''
# Diversity and Representation in Hollywood
'''
from PIL import Image

image = Image.open('movie_reel.png')
st.image(image, use_column_width=True)
'''
## Select a movie to view
'''
title = st.text_input('Movie title')

st.write('The current movie title is', title)

if title != "":
    df = pd.read_csv('raw_data/man_of_steel_results.csv')
    st.write(df['frame_number'][0])
