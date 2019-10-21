# -*- coding: utf-8 -*-
import re
import scrapy

from ..items import MovieItem


class Zy35Spider(scrapy.Spider):
    name = 'zy35'
    allowed_domains = ['3514.com']
    start_urls = ['http://3514.com/']

    def start_requests(self):
        url=self.start_urls[0]
        yield scrapy.Request(url,callback=self.parse)

    def get_list(self,response):
        print(response)

    def parse(self, response):
        html=response.body.decode('utf8')
        detail_urls=re.findall('<li><span class="tt"></span><span class="xing_vb4"><a href="(.*?)" target="_blank">(.*?)</a>',html,re.S)
        for url in detail_urls:
            name=url[1]
            uri=self.start_urls[0]+url[0]
            yield scrapy.Request(uri,callback=self.parse_detail,meta={'name':name})

    def parse_detail(self,response):
        html=response.body.decode('utf8')
        play_url=re.findall('第1集\$(.*?)</a>',html,re.S)
        img=re.findall('<img class="lazy" src="(.*?)" alt=',html,re.S)

        # name=response.meta.get('name')
        item = MovieItem()
        item['d_playurl'] = play_url[0]
        item['d_pic'] = img[0]
        item['d_remarks'] = u'高清'
        item['d_name'] = response.meta.get('name')
        item['d_type'] = 19
        item['d_playfrom'] = 'm3u8'
        yield item