from pickle import TRUE
import scrapy

#Titulo = //h1/a/text()
#Citas = //span[@class="text" and @itemprop="text"]/text()
#Top ten tags = //div[contains(@class, "tags-box")]//span[@class"tag-item"]/a/text()
#Next page button =  '//ul[@class="pager"]//li[@class="next"]/a/@href'
#Author = //small[@class="author" and @itemprop="author"]/text()


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST':24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['bryhan@fedora.pe'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'PepitoMartinez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }


    def parse_ony_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            #author = kwargs['author']

        new_quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        new_author = response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall()
        quotes.extend(list(zip(new_quotes, new_author)))



        #author = response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall()



        #quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())


        next_page_buttom_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_buttom_link:
            yield response.follow(next_page_buttom_link, callback=self.parse_ony_quotes, cb_kwargs= {'quotes': quotes})

        else:
            yield{
                'quotes': quotes,
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class="tag-item"]/a/text()').getall()       

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags,
        }


        next_page_buttom_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_buttom_link:
            yield response.follow(next_page_buttom_link, callback=self.parse_ony_quotes, cb_kwargs= {'quotes': quotes})

#scrapy crawl quotes -a top=7 activar