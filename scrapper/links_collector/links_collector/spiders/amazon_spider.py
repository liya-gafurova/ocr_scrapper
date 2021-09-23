import scrapy
from scrapy.spiders import Rule




class QuotesSpider(scrapy.Spider):
    name = "amazon"
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]
    def __init__(self):
        self.links = []


    def parse(self, response):
        self.links.append(response.url)
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse)