# -*- coding: utf-8 -*-

from scrapy import Request
from ..items import *

class SogouWordSpdSpider(scrapy.Spider):
    name = 'sogou_word_spd'
    # allowed_domains = ['sogou.com']
    start_urls = ['https://pinyin.sogou.com/dict/cate/index/167']

    def parse(self, response):
        # 一级分类名 和 url
        type_list = ['城市信息', '自然科学', '社会科学', '工程应用', '农林渔畜', '医学医药', '电子游戏', '艺术设计', '生活百科', '运动休闲', '人文科学', '娱乐休闲']
        type_url_list = response.xpath('//*[@id="dict_nav_list"]/ul/li/a/@href').extract()
        for i in range(len(type_url_list)):
            url = 'http://pinyin.sogou.com' + type_url_list[i]
            yield Request(url, callback=self.parse_further, dont_filter=True, meta={'type1': type_list[i]})


    def parse_further(self, response):
        # 二级分类名 和 url
        type1 = response.meta['type1']

        type2_list = response.xpath('//*[@class="cate_no_child no_select"]') + response.xpath('//*[@class="cate_has_child no_select"]')
        for node in type2_list:
            type2 = node.xpath('./a//text()').extract()[0] + node.xpath('./a//text()').extract()[1]
            url = 'http://pinyin.sogou.com' + node.xpath('./a/@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_further2, dont_filter=True, meta={'type1': type1, 'type2': type2})


    def parse_further2(self, response):
        # 具体分类名 和 下载的url
        item = SogouwordspiderItem()
        type1 = response.meta['type1']
        type2 = response.meta['type2']

        url_list = response.xpath('//*[@class="dict_detail_block"]') + response.xpath('//*[@class="dict_detail_block odd"]')
        for node in url_list:
            title = node.xpath('./div[1]/div/a/text()').extract()[0]
            item['url'] = node.xpath('./div[2]/div[2]/a/@href').extract()[0]
            filename = '{}_{}_{}'.format(type1, type2, title)
            item['filename'] = self.strip_wd(filename)
            item['type1'] = type1
            item['type2'] = type2
            yield item

        next_page = response.xpath('//div[@id="dict_page_list"]//span/a[contains(text(),"下一页")]/@href')
        if next_page:
            url = 'http://pinyin.sogou.com' + next_page.extract()[0]
            yield Request(url, callback=self.parse_further2, dont_filter=True, meta={'type1': type1, 'type2': type2})



    def strip_wd(self, s):
        '''
        去除字符串中的非法字符
        '''
        kwd = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '(', ')','（', '）', '.', '/', '|', '>', '<', '\\', '*', '"', '“', ]
        ans = ''
        for i in s:
            if i not in kwd:
                ans += i
        return ans
