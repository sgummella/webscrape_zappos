# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZapposItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Product  = scrapy.Field()
    Price = scrapy.Field()
    True_size_feeling = scrapy.Field()
    True_width_feeling = scrapy.Field()
    Arch_support = scrapy.Field()
    Overall_rating = scrapy.Field()
    Comfort_rating = scrapy.Field()
    Style_rating = scrapy.Field()
    Fit_sm_lg = scrapy.Field()
    Fit_na_wd = scrapy.Field()
    Fit_arch_support = scrapy.Field()
    Review_text = scrapy.Field()
