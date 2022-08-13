import scrapy


class YatubeSpider(scrapy.Spider):
    name = 'yatube'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']

    def parse(self, response):
        pass
