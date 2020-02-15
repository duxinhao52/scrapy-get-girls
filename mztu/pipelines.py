# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem #检查item是否完整
from scrapy.pipelines.images import ImagesPipeline
#图片管道里下载单张图片（有特定的命名字段）
class MztuPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        headers = {
            'referer': 'https://www.mzitu.com//all'
        }
        yield scrapy.Request(item['image_url'], headers=headers, meta={'item':item})
    def item_completed(self,results,item,info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item #后续仍要用item，故要返回出去
    #图片目录路径！
    def file_path(self,request,response=None,info=None):
        category=request.meta['item']['category']
        image_name=request.meta['item']['image_url'].split('/')[-1] #这个该死的split我查它查了四五个小时！！！
        return '%s/%s' % (category,image_name)
        
