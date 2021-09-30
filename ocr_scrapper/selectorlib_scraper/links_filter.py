import re
from typing import List

bestsellers_pattern = re.compile('/gp/bestsellers')


def filter_unique_links(links: List[str]):
    return list(set(links))


def filter_best_sellers_urls(link):
    found_group = re.search(bestsellers_pattern, link)
    return False if found_group is None else True


