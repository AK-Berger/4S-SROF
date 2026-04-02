"""Helpers used by the analysis_workflow notebook."""

from pathlib import Path
import shutil

import cv2
import natsort
import numpy as np


def find_reds(pic):
    red_xs = np.where(pic[:, :, 0] != pic[:, :, 1])[1]
    red_ys = np.where(pic[:, :, 0] != pic[:, :, 1])[0]
    return red_xs, red_ys


def rotate_image(image, angle):
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    return cv2.warpAffine(image, rotation_matrix, (width, height))


def load_files(ad):
    files = [path.name for path in Path(ad).iterdir() if path.suffix.lower() == ".tif"]
    return natsort.natsorted(files)


def slope_measurement(ad):
    slope_dir = Path(ad) / "slope"
    pic_slope1 = cv2.imread(str(slope_dir / "1.bmp"))
    pic_slope2 = cv2.imread(str(slope_dir / "2.bmp"))

    red1_xs, red1_ys = find_reds(pic_slope1)
    red2_xs, red2_ys = find_reds(pic_slope2)
    dx = red2_xs - red1_xs
    dy = red2_ys - red1_ys
    gradian = np.arctan(dy / dx)
    angle = gradian * 180 / np.pi
    rotated1 = rotate_image(pic_slope1, angle[0])
    return angle[0], rotated1, red1_xs[0], red1_ys[0], red2_xs[0], red2_ys[0]


def make_folders(ad):
    base_path = Path(ad)
    for folder_name in ("SR_edge", "SR_result"):
        folder_path = base_path / folder_name
        if folder_path.exists():
            shutil.rmtree(folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
