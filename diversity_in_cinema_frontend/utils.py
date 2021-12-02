from google.cloud import storage
import re
import pandas as pd
from tqdm import tqdm
from diversity_in_cinema_frontend.params import *
from diversity_in_cinema_frontend.api import fetch_movie_basic_data
from diversity_in_cinema_frontend.api import fetch_movie_details


def get_movie_list(subfolders):
    """
    Function ro grab file names from a GCP bucket directory
    Parameters:
    bucket_name: Name of GCP bucket
    subfolders: complete subfolder path as a string where file names should
                be retrieved from in the format folder_1/folder_2/.../folder_n
    """

    # check if movie was already processed:

    client = storage.Client()
    file_names = [str(x).split(f"{subfolders}/")[1].\
        split("/statistics")[0].\
            replace("_", " ")\
                for x in \
                    client.list_blobs(BUCKET_NAME_STREAMLIT, prefix=subfolders)]
    # replace first entry with empty str
    file_names[0] = ""

    return file_names


def get_evolution_data():

    df_stats_list = []

    regex = re.compile(r'\((\d{4})\)')

    movie_list = get_movie_list("CSVs")[1:]

    for movie in tqdm(movie_list):

        movie = movie.replace(" ", "_")

        if movie == "":
            continue

        year = regex.findall(movie)[0]

        df = pd.read_csv(
            f"gs://{BUCKET_NAME_STREAMLIT}/CSVs/{movie}/statistics",
            index_col=None)

        df["title"] = movie
        df["year"] = year

        df["year"] = pd.to_datetime(df["year"].values)
        df.sort_values("year", inplace=True)
        df_stats_list.append(df)

    df_stats_total = pd.concat(df_stats_list, axis=0)
    df_stats_total.sort_values("year", inplace=True)

    def add_revenue(column):

        column = column.replace("_", " ")
        return fetch_movie_details(column).get("revenue", None)

    def add_runtime(column):

        column = column.replace("_", " ")
        return fetch_movie_details(column).get("runtime", None)

    df_stats_total["revenue"] = df_stats_total["title"].apply(add_revenue)
    df_stats_total["runtime"] = df_stats_total["title"].apply(add_runtime)

    return df_stats_total.reset_index()


if __name__ == "__main__":
    # print(get_movie_list("CSVs"))
    get_evolution_data()
