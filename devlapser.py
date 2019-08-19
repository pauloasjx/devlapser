import os
import datetime

from grabber import make_movie

movie_name = make_movie()
now = datetime.datetime.now().strftime("%B %d, %Y")
title = f"Dev - {now}"

os.system(f'youtube-upload --title="{title}" --privacy="private" {movie_name}')
