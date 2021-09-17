from dataclasses import dataclass, asdict
from typing import List
import os
import argparse


from ocr_scrapper.settings import FILES_DIR, SCREENSHOTS_DIR_NAME, TEXTS_DIR_NAME

@dataclass
class Recourse:
    name: str
    links: List[str]


@dataclass
class OutDirectories:
    screenshots: str
    texts: str

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