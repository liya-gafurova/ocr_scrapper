import datetime
import json

from PIL import Image
import pytesseract
from selenium import webdriver

from ocr_scrapper.helpers import *


def load_webdriver():
    return webdriver.Firefox()


def explore_resource(driver, resource, screenshots_directory):
    for url in resource.links:
        driver.get(url)
        driver.save_screenshot(f'{screenshots_directory}/scr_{datetime.datetime.now()}.png')

    driver.close()


def recognize_screenshots(screenshots_directory, recognized_texts_directory):
    for screenshot_file in os.listdir(screenshots_directory):
        image_file = screenshots_directory + screenshot_file
        screenshot_name = get_filename_without_extension(screenshot_file)
        data = {'texts': get_texts_from_areas(image_file)}
        with open(f"{recognized_texts_directory}{screenshot_name}.json", 'w') as text_file:
            text_file.write(json.dumps(data))


if __name__ == '__main__':
    args = parse_cli_args()

    dataset = load_recourse_dataset('./links/amazon.txt')
    dirs = create_out_directories(dataset.name)

    if args.mode == 'scrape':
        web_driver = load_webdriver()
        explore_resource(web_driver, dataset, dirs.screenshots)

    elif args.mode == 'recognize':
        recognize_screenshots(dirs.screenshots, dirs.texts)
