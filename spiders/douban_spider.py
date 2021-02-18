# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import DoubanItem


# 命令
# 生成 spider py文件：scrapy genspider +name +url
# 生成csv文件：scrapy crawl spider文件名 -o csv文件名

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        # 获取整个数据的匹配结果
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        # 通过循还匹配，形成json字符串
        for item in movie_list:
            douban_item = DoubanItem()
            douban_item['number'] = item.xpath(".//div[@class='pic']/em/text()").extract_first()
            douban_item['name'] = item.xpath(".//div[@class='hd']//a//span[1]/text()").extract_first()
            intraduce = item.xpath(".//div[@class='info']//div[@class='bd']//p[1]//text()").extract()
            for i in intraduce:
                intrd = "".join(i.split())
                douban_item['intrd'] = intrd
            douban_item['point'] = item.xpath(".//div[@class='star']//span[@class='rating_num']/text()").extract_first()
            douban_item['comment'] = item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['discribe'] = item.xpath(".//div[@class='bd']//p[@class='quote']//span/text()").extract_first()
            # 将数据yiled到pipelines里面去
            yield douban_item
        # 模仿翻页爬取
        next_link = response.xpath(".//span[@class='next']//link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
