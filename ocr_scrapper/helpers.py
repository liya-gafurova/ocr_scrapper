from dataclasses import dataclass, asdict
from typing import List
import os
import argparse

import cv2
import pytesseract

from ocr_scrapper.settings import FILES_DIR, SCREENSHOTS_DIR_NAME, TEXTS_DIR_NAME


@dataclass
class Recourse:
    name: str
    links: List[str]


@dataclass
class OutDirectories:
    screenshots: str
    texts: str


@dataclass
class Block:
    text: str
    box: List[int]


@dataclass
class DatasetStructure:
    screenshot: str
    blocks: List[Block]


def get_filename_without_extension(get_screenshot_filename):
    return os.path.splitext(get_screenshot_filename)[0]


def create_out_directories(recourse_name: str) -> OutDirectories:
    screenshots_dir = f'{FILES_DIR}{recourse_name}{SCREENSHOTS_DIR_NAME}'
    recognized_texts_dir = f'{FILES_DIR}{recourse_name}{TEXTS_DIR_NAME}'
    out_dirs = OutDirectories(screenshots=screenshots_dir, texts=recognized_texts_dir)

    for directory in asdict(out_dirs).values():
        if not os.path.exists(directory):
            os.makedirs(directory)

    return out_dirs


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode')
    arguments = parser.parse_args()

    return arguments


def load_recourse_dataset(recourse_filepath: str) -> Recourse:
    recourse_name = get_filename_without_extension(os.path.basename(recourse_filepath))
    with open(recourse_filepath) as links_file:
        links = links_file.readlines()

    return Recourse(name=recourse_name, links=links)


def get_areas(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    return contours


def crop_region(image, region):
    x, y, w, h = cv2.boundingRect(region)
    return image[y:y + h, x:x + w]


def get_box(image, contour):
    # method mock
    return [0, 0, 0, 0]


def get_texts_from_areas(image: str, contours: list) -> List[Block]:
    blocks = []
    for contour in contours:
        blocks.append(
            Block(text=pytesseract.image_to_string(crop_region(image, contour)),
                  box=get_box(image, contour))
        )
    return blocks


def get_text_blocks(img_path) -> List[Block]:
    image = cv2.imread(img_path)
    contours = get_areas(image)
    return get_texts_from_areas(image, contours)
