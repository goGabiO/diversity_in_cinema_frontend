from google.cloud import storage
from diversity_in_cinema_frontend.params import *

def get_movie_list():
    # check if movie was already processed:
    client = storage.Client()
    processed_movies = [str(x).split(",")[1].\
        replace("_", " ").\
            replace("CSVs/", "").\
                split("/")[0].\
                    strip() for x in client.\
                        list_blobs(BUCKET_NAME_STREAMLIT, prefix='CSVs')]
    return processed_movies

if __name__ == "__main__":

    print(get_movie_list())
