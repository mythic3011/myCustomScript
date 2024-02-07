import os
import moviepy.editor as mp
from moviepy.editor import vfx

local_path = os.path.dirname(os.path.abspath(__file__))


def speed_up_gif(gif_path):
    clip = mp.VideoFileClip(gif_path)
    clip = clip.fx(vfx.speedx, 2)
    clip.write_gif(gif_path)


gif_files = [f for f in os.listdir(local_path) if f.endswith('.gif')]

for gif_file in gif_files:
    gif_path = os.path.join(local_path, gif_file)
    speed_up_gif(gif_path)
