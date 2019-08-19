import av
import cv2
import pyscreenshot
import subprocess
import numpy as np

import os
import shutil
import string
import random
from tqdm import tqdm

from time import sleep


def resize_photo(photo, resize):
    height, width = photo.shape[:2]

    photo_resized = cv2.resize(
        photo,
        (int(resize * width), int(resize * height)),
        interpolation=cv2.INTER_CUBIC,
    )

    return photo_resized


def get_screen_size():
    screen = pyscreenshot.grab()
    screen = np.array(screen)

    screen_size = screen.shape[:2]

    return screen_size


def get_screen():
    screen = pyscreenshot.grab().convert("RGB")
    screen = np.array(screen)[..., ::-1]

    return screen


def get_cam(cam):
    _, photo = cam.read()
    photo = np.array(photo)

    return photo


def random_string(length):
    generated_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    return generated_string


def make_frame(photo, screen):
    photo = resize_photo(photo, 0.3)
    screen[0: photo.shape[0], 0: photo.shape[1], 0: photo.shape[2]] = photo

    frame_c = np.asarray(screen, order="C")

    frame = av.VideoFrame.from_ndarray(frame_c, format="bgr24")

    return frame


def make_movie(delay=2, callback=None):
    cam = cv2.VideoCapture(0)

    movie_name = random_string(8)

    if not os.path.exists(movie_name):
        os.makedirs(movie_name)

    try:
        subprocess.run(["./bin/devlapser", movie_name])

    except KeyboardInterrupt:
        screen_size = get_screen_size()

        video = av.open(f"{movie_name}.mp4", "w")
        stream = video.add_stream("mpeg4", "23.976")
        stream.width = screen_size[1]
        stream.height = screen_size[0]
        #stream.pix_fmt = "yuv420p"

        number_photos = int(len(os.listdir(movie_name)) / 2)

        for counter in tqdm(range(number_photos)):
            photo = cv2.imread(f"{movie_name}/{counter}_cam_image.jpg")
            screen = cv2.imread(f"{movie_name}/{counter}_screen_image.jpg")

            frame = make_frame(photo, screen)
            packet = stream.encode(frame)
            video.mux(packet)

        shutil.rmtree(f"{movie_name}")

        cam.release()
        video.close()

        if callback:
            callback()

        return f"{movie_name}.mp4"
