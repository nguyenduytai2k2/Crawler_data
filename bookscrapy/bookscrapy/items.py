# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookscrapyItem(scrapy.Item):
    BookUrl = scrapy.Field()
    product_main = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    star = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_exc = scrapy.Field()
    price_inc = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    nor = scrapy.Field()
    type_of_book = scrapy.Field()
    description = scrapy.Field()