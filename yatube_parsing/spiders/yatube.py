import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = 'yatube'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'yatube_parsing.pipelines.MondayPipeline': 300
        }
    }

    def parse(self, response):
        for citation in response.css('div.card-body'):
            data = {
                'author': citation.css('a strong::text').get(),
                'text': ''.join(citation.css('p::text').getall()).strip(),
                'date': citation.css('small.text-muted::text').get(),
            }
            yield YatubeParsingItem(data)
        next_page = response.css('a:contains("Следующая")::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
