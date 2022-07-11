import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    def parse(self, response):
        print('*' * 10)
        print('\n\n')
        print(response.status, response.headers)
        print('*' * 10)
        print('\n\n')

