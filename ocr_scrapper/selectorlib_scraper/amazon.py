import random

from selectorlib import Extractor
import requests
import json
from time import sleep

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('pages_with_products.yml')
e2 = Extractor.from_yaml_file('test.yml')


def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cokkie': 'session-id=135-3356242-5553934; sp-cdn="L5Z9:RU"; ubid-main=134-8173956-2865144; session-id-time=2082787201l; i18n-prefs=USD; lc-main=en_US; session-token=+mhTBVbtzi4gBWs0vYhP1oHjHJh06dhmMddO+xlPpYRVxhN69HvwBx0gZIJPNWMEHM47cgc8e72aIJCjOQiRSbcv0rF7fpoa/vjCzHyGRRQ/KpKc7iMKQs1X4VbjfSoOrUSu1+Yo1H6y4mfjoXrmteJIxuRRqduSzf3AWFZrIAtzyCzIYoiWeKplOHOS3BWq; skin=noskin',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
            return None
        # Pass the HTML of the page and create
    return e2.extract(r.text)
# product_data = []

with open("urls.txt", 'r') as urllist, open('output2.jsonl', 'w') as outfile:
    for url in urllist.readlines():
        data = scrape(url)
        if data:
            json.dump(data, outfile)
            outfile.write("\n")
            print(data)
        sleep(random.randint(5,10))


# TODO add getting product link from PRODUCTS_LIST links

