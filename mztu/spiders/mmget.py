# -*- coding: utf-8 -*-
import scrapy
from mztu.items import MztuItem

class MmgetSpider(scrapy.Spider):
    name = 'mmget'
    start_urls = ['https://www.mzitu.com//all']

    def parse(self, response):
        #获取套图链接！！
        imagegroups=response.xpath("//ul[@class='archives']/li/p/a/@href").getall()
        for imagegroup in imagegroups:
            yield scrapy.Request(url=imagegroup,callback=self.group_parse)
    def group_parse(self,response):
        #获取组图中的所有图片！！
        image_url=response.xpath("//div[@class='main-image']/p/a/img/@src").get()
        image_url_topic=response.xpath("//div[@class='main-image']/p/a/img/@alt").get() #每张图片都要有主题目录
        next_image_url=response.xpath("//div[@class='pagenavi']/a/@href").getall()[-1] #下一张图片的链接
        flag=response.xpath("//div[@class='pagenavi']/a/span/text()").getall()[-1]
        item=MztuItem()
        item['category']=image_url_topic
        item['image_url']=image_url
        yield item
        if '下一页' in flag:
            yield scrapy.Request(url=next_image_url,callback=self.group_parse)

