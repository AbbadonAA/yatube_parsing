import scrapy


class YatubeSpider(scrapy.Spider):
    name = 'yatube'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']

    def parse(self, response):
        for citation in response.css('div.card-body'):
            yield {
                'author': citation.css('a strong::text').get(),
                'text': ''.join(citation.css('p::text').getall()).strip(),
                'date': citation.css('small.text-muted::text').get(),
            }
        next_page = response.css('a:contains("Следующая")::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
