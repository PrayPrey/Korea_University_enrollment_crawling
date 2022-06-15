# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Enrolment3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    entire = scrapy.Field()
    campus = scrapy.Field()
    number = scrapy.Field()
    class_ = scrapy.Field()
    seperate = scrapy.Field()
    major = scrapy.Field()
    class_name = scrapy.Field()
    prof= scrapy.Field()
    time= scrapy.Field()
    place = scrapy.Field()
