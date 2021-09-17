import datetime
import os
from PIL import Image
import pytesseract
from selenium import webdriver

from ocr_scrapper.helpers import get_filename_without_extension, load_recourse_dataset, create_out_directories, \
    parse_cli_args


def load_webdriver():
    return webdriver.Firefox()


def explore_resource(driver, resource, screenshots_directory):
    for url in resource.links:
        driver.get(url)
        driver.save_screenshot(f'{screenshots_directory}/scr_{datetime.datetime.now()}.png')

    driver.close()


def recognize_screenshots(screenshots_directory, recognized_texts_directory):
    for screenshot_file in os.listdir(screenshots_directory):
        recognized_text = pytesseract.image_to_string(Image.open(screenshots_directory + screenshot_file))
        screenshot_name = get_filename_without_extension(screenshot_file)
        with open(f"{recognized_texts_directory}{screenshot_name}.txt", 'w') as text_file:
            text_file.write(recognized_text)


if __name__ == '__main__':
    dataset = load_recourse_dataset('./links/amazon.txt')
    dirs = create_out_directories(dataset.name)
    args = parse_cli_args()

    if args.mode == 'scrape':
        web_driver = load_webdriver()
        explore_resource(web_driver, dataset, dirs.screenshots)

    elif args.mode == 'recognize':
        recognize_screenshots(dirs.screenshots, dirs.texts)
