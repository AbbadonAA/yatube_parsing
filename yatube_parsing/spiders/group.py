import scrapy


class GroupSpider(scrapy.Spider):
    name = 'group'
    allowed_domains = ['51.250.32.185']
    start_urls = ['http://51.250.32.185/']

    def parse_group(self, response):
        yield {
            'group_name': response.css('div.card-body h2::text').get().strip(),
            'description': response.css(
                'p.group_descr::text').get().strip().replace('\u200b', ''),
            'posts_count': int(response.css(
                'div.h6::text').get().strip().replace('Записей: ', '')),
        }

    def parse(self, response):
        groups = response.css('a.group_link::attr(href)').getall()
        for group_link in groups:
            yield response.follow(group_link, callback=self.parse_group)
        next_page = response.css('a:contains("Следующая")::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
