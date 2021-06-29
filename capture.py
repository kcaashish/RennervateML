import os
import bz2
import requests
from tqdm import tqdm
import cv2

# creating an object, zero for external camera
cap = cv2.VideoCapture(0)

A = 0

if cap.isOpened():
    CHECK, frame = cap.read()
else:
    CHECK = False

url = "https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2"
local_filename = url.split("/")[-1]

if not os.path.exists(local_filename):
    response = requests.get(url, stream=True)
    length = response.headers.get("content-length", 0)
    print(length)
    with tqdm.wrapattr(
        open(local_filename, "wb"),
        "write",
        miniters=1,
        desc="Downloading ",
        total=int(length),
    ) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)

dat_file = local_filename[:-4]
if not os.path.exists(dat_file):
    with tqdm.wrapattr(
        open(dat_file, "wb"), "write", miniters=1, desc="Extracting "
    ) as uncompressed_file, open(local_filename, "rb") as file:
        bz2_decompressor = bz2.BZ2Decompressor()
        for data in iter(lambda: file.read(100 * 1024), b""):
            uncompressed_file.write(bz2_decompressor.decompress(data))

# # for photo capture
# img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Image", img)
# cv2.waitKey(0)

cv2.namedWindow("Capturing")

# for video capture
while CHECK:
    A = A + 1

    # creating a frame object
    CHECK, frame = cap.read()
    # print(CHECK)
    # print(frame)

    # converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show the frame
    cv2.imshow("Capturing", gray)
    # cv2.imshow("Normal", frame)

    # for playing
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

# print(A)

cv2.destroyAllWindows()

# shut down camera
cap.release()
