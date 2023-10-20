import os
import time
import typing
import shutil
import numpy as np
from PIL import Image
from absl import logging
from mediapy import mediapy as media


_CONFIG_FFMPEG_NAME_OR_PATH = 'ffmpeg'
_Path = typing.Union[str, os.PathLike]

# Set logging verbosity to print to console
logging.set_verbosity(logging.INFO)

def get_ffmpeg_path() -> str:
    path = shutil.which(_CONFIG_FFMPEG_NAME_OR_PATH)
    if not path:
      raise RuntimeError(
          f"Program '{_CONFIG_FFMPEG_NAME_OR_PATH}' is not found;"
          " perhaps install ffmpeg using 'apt-get install ffmpeg'.")
    return path

def create_video(framesdir: _Path, fps: int):
    ffmpeg_path = get_ffmpeg_path()
    media.set_ffmpeg(ffmpeg_path)
    logging.info('reading frames')
    start = time.time()
    frames = list(np.array(Image.open(os.path.join(framesdir, img))) for img in sorted(os.listdir(framesdir)) if img.endswith(".png"))
    vidlength = len(os.listdir(framesdir))
    logging.info(f'..Writing video to {framesdir}/interpolated.mp4')
    media.write_video(f'{framesdir}/interpolated.mp4', frames, vidlength, fps=fps)
    logging.info(f'Output video saved at {framesdir}/interpolated.mp4.')
    end = time.time()
    logging.info(f'Created output in {end-start:.2f}')
