from google.cloud import storage
from diversity_in_cinema_frontend.params import *

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
        split("/statistics")[0]\
            for x in \
                client.list_blobs(BUCKET_NAME_STREAMLIT, prefix=subfolders)]
    # replace first entry with empty string
    file_names[0] = ""

    return file_names


if __name__ == "__main__":

    print(get_movie_list("CSVs"))
