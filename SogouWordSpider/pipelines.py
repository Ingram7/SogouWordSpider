# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

# 下载文件
class SogouWordFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'], meta={'item': item})

    # 下载完成时调用
    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            print('下载失败')
            raise DropItem("Item contains no files")
        print('下载成功')
        return item

    # 文件名
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # basedir = os.getcwd()
        # download_dir = os.path.join(basedir, 'download')
        # path = os.path.join(download_dir, item['filename'] + '.scel')
        path = item['filename'] + '.scel'
        return path