import datetime
from urllib.parse import urlparse
import os
from PIL import Image
import pytesseract

from selenium import webdriver

from ocr_scrapper.settings import FILES_DIR, SCREENSHOTS_DIR_NAME, TEXTS_DIR_NAME

resource = 'https://www.amazon.com/Acer-AN515-55-53E5-i5-10300H-GeForce-Keyboard/dp/B092YHJGMN/ref=sr_1_6?dchild=1&fst=as%3Aoff&pd_rd_r=5767899b-b013-427d-b07b-be012f0ce856&pd_rd_w=orQky&pd_rd_wg=p8bed&pf_rd_p=83ab1c34-7657-4d09-b72d-0a3e4b634b1d&pf_rd_r=9KERWJJZT62V1EC5ED1Q&qid=1631773550&rnid=16225007011&s=computers-intl-ship&sr=1-6'
screenshots_dir = f'{FILES_DIR}{urlparse(resource).hostname}{SCREENSHOTS_DIR_NAME}'
recognized_texts_dir = f'{FILES_DIR}{urlparse(resource).hostname}{TEXTS_DIR_NAME}'
DATA_DIRS = [screenshots_dir, recognized_texts_dir]

for directory in DATA_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_webdriver():
    return webdriver.Firefox()


def explore_resource(web_driver, resource, screenshots_dir):
    web_driver.get(resource)
    web_driver.save_screenshot(f'{screenshots_dir}/scr_{datetime.datetime.now()}.png')

    web_driver.close()


def recognize_screenshots(screenshots_dir, recognized_texts_dir):
    for screenshot in os.listdir(screenshots_dir):
        screenshot_name = os.path.splitext(screenshot)[0]
        recognized_text = pytesseract.image_to_string(Image.open(screenshots_dir + screenshot))
        with open(recognized_texts_dir + screenshot_name + '.txt', 'w') as text_file:
            text_file.write(recognized_text)


if __name__ == '__main__':
    # Get Pictures
    # web_driver = load_webdriver()
    # explore_resource(web_driver, resource, screenshots_dir)

    # Recognize Pictures
    recognize_screenshots(screenshots_dir, recognized_texts_dir)
