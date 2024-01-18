# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class DatascraperItem(scrapy.Item):
#     # define the fields for your item here like:
    name = scrapy.Field()
    pass
def serialize_price(value):
        return f'£{str(value)}'
# class HomeItem(Item):
#     title = Field()
#     price = Field ()

# class BookItem(scrapy.Item):
    #this is attribute (alonhadat)
    # title = scrapy.Field()
    # date_post = scrapy.Field()
    # description = scrapy.Field()
    # url = scrapy.Field()
    # price = scrapy.Field()
    # square = scrapy.Field()
    # address = scrapy.Field()
    # contact_name = scrapy.Field()
    # contact_phone = scrapy.Field()
    # #contact_star_rate = scrapy.Field()
    # contact_profile = scrapy.Field()
    # direction = scrapy.Field()
    # dining = scrapy.Field()
    # type_content = scrapy.Field()
    # homefront = scrapy.Field()
    # kitchen = scrapy.Field()
    # home_type = scrapy.Field()
    # legal = scrapy.Field()
    # roof_top =  scrapy.Field()
    # width = scrapy.Field()
    # height = scrapy.Field()
    # number_floor = scrapy.Field()
    # gara = scrapy.Field()
    # number_bedroom = scrapy.Field()
    # owner = scrapy.Field()
 
    # title = scrapy.Field()
    # date_post = scrapy.Field()
    # description = scrapy.Field()
    # # url = scrapy.Field()
    # price = scrapy.Field()
    # square = scrapy.Field()
    # contact_email = scrapy.Field()
    # contact_name = scrapy.Field()
    # contact_phone = scrapy.Field()

