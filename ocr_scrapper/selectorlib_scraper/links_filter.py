import json
import re
from typing import List

customer_reviews = re.compile('#customerReviews')  # Not
offering_list = re.compile('/gp/offer-listing')  # Not

NOT_patterns = [customer_reviews, offering_list]


# функициональное программирование? - map/reduce - изучить

def filter_unique_links(links: List[str]):
    return list(set(links))


def filter_url_by_pattern(pattern, link, should_contain):
    found_pattern = True if re.search(pattern, link) else False
    return found_pattern == should_contain


def filter_url_by_all_patterns(patterns, link, should_contain=False):
    ulr_not_containing_bad_patterns: List[bool] = [filter_url_by_pattern(pattern, link, should_contain)
                                                   for pattern in patterns]
    return all(ulr_not_containing_bad_patterns)


def filter_links(links_list: List[str]) -> List[str]:
    unique_links = filter_unique_links(links_list)
    filtered_links = [link for link in unique_links if
                      filter_url_by_all_patterns(NOT_patterns, link, should_contain=False)]
    return filtered_links


with open('output.jsonl', 'r') as links_data, open('filtered_links.json', 'w') as outfile2:
    json_data = json.loads(links_data.read())
    links = json_data.get('link')
    print(links)

    filtered = filter_links(links)
    print(filtered)
    outfile2.write(
        json.dumps(
            {
                'link': filtered
            }
        )
    )
