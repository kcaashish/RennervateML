import os
import time
import requests
from tqdm import tqdm


def download_detector():
    "downloading the required dlib 68 landmarks predictor"
    url = "https://github.com/JeffTrain/selfie/raw/master/shape_predictor_68_face_landmarks.dat"
    local_filename = url.split("/")[-1]

    if not os.path.exists(local_filename):
        response = requests.get(url, stream=True)
        length = response.headers.get("content-length", 0)
        print("Downloading the shape predictor file:")
        with tqdm.wrapattr(
            open(local_filename, "wb"),
            "write",
            miniters=1,
            desc="Downloading file ",
            total=int(length),
        ) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
        print("Download complete!")
        time.sleep(0.1)
