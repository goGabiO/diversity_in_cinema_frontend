import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt

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
p {
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
    tag = f'<img src="data:faces/webp;base64,{encoded}">'
    return tag


def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:faces/webp;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style


image_path = 'faces.webp'
image_link = '~/code/moe221/diversity_in_cinema_frontend/'

st.write(background_image_style(image_path), unsafe_allow_html=True)

'''
# Diversity and Representation in Hollywood
'''
from PIL import Image

image = Image.open('movie_reel.png')
st.image(image, use_column_width=True, output_format="PNG")
'''
## Select a movie to view
'''
option = st.selectbox('', ('Man of Steel', 'Ace Ventura'))

st.write('You selected:', option)

with st.container():
    if option != "":
        search_terms = option.lower().split()
        movie_name = '_'.join(search_terms)
        file_name = f'raw_data/{movie_name}_results.csv'
        df = pd.read_csv(file_name)
        x = df["gender"].value_counts().index
        y = df["gender"].value_counts().values
        st.write('Statistics from:', movie_name)
        fig, ax = plt.subplots()
        plt.bar(x, y)
        st.pyplot(fig)
