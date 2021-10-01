import re
from typing import List

customer_reviews = re.compile('#customerReviews')  # Not
offering_list = re.compile('/gp/offer-listing')  # Not

NOT_patterns = [customer_reviews, offering_list]


def filter_unique_links(links: List[str]):
    return list(set(links))


def filter_url_by_pattern(pattern, link, should_not_contain=False):
    found_group = re.search(pattern, link)
    return found_group is None and should_not_contain


def filters_links(links_list: List[str]) -> List[str]:
    unique_links = filter_unique_links(links_list)
    filtered_links = [link for link in unique_links if filter_unique_links(link, NOT_patterns)]
    return filtered_links
