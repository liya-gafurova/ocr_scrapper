import scrapy


class QuotesSpider(scrapy.Spider):
    name = "amazon"

    def start_requests(self):
        URLs = ["https://www.amazon.com/b?node=16225009011&pf_rd_r=9BWSJ1HB0HBXZ1NMZZJ3&pf_rd_p=5232c45b-5929-4ff0-8eae-5f67afd5c3dc&pd_rd_r=d8b98471-6bcf-4094-b8dd-4108a4d83da4&pd_rd_w=cH3eF&pd_rd_wg=vnoNK&ref_=pd_gw_unk"]
        for url in URLs:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')