# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SogouwordspiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = Field()        # 词库下载url
    filename = Field()   # 文件名
    type1 = Field()      # 一级分类名
    type2= Field()       # 二级分类名

