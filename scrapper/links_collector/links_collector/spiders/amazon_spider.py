import scrapy
from scrapy.spiders import Rule


class LinkExtractor:
    pass


class QuotesSpider(scrapy.Spider):
    name = "amazon"
    start_urls = [
        "https://www.amazon.com/b?node=16225009011&pf_rd_r=9BWSJ1HB0HBXZ1NMZZJ3&pf_rd_p=5232c45b-5929-4ff0-8eae-5f67afd5c3dc&pd_rd_r=d8b98471-6bcf-4094-b8dd-4108a4d83da4&pd_rd_w=cH3eF&pd_rd_wg=vnoNK&ref_=pd_gw_unk"]
    # rules = [Rule(LinkExtractor(), callback='parse', follow=True)]


    def parse(self, response):
        for link in response.xpath('//div/p/a'):
            yield {
                "link": self.base_url + link.xpath('.//@href')
            }