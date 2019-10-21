# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    d_name = scrapy.Field()
    d_playurl = scrapy.Field()
    d_pic = scrapy.Field()
    d_remarks = scrapy.Field()
    d_playfrom = scrapy.Field()
    d_type = scrapy.Field()



