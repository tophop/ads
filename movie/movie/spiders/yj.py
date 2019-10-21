# -*- coding: utf-8 -*-
import random
import re

import time
from lxml import etree

import requests
import scrapy
import scrapy

from ..items import MovieItem


def get_ua():
    ua_list = []
    with open('ua.txt', 'r') as f:
        txt = f.read().split('\n')
    text = list(txt)
    for i in text:
        try:
            ua = i.split(':')[1]
            ua_list.append(ua)
        except:
            pass
    return ua_list
class YjSpider(scrapy.Spider):
    # @classmethod

    ua_list=get_ua()
    ua=random.choice(ua_list)
    name = 'yj'
    allowed_domains = ['www.1999.com:999']
    start_urls = ['http://www.1999.com:999/']
    a={'User-Agent':ua}
    url_list = []
    try:

        res = requests.get(url=start_urls[0], headers=a).text
        txet = res
        new_url = re.findall('var ul = (.*?);', ''.join(txet.split('\r\n')))
        a_list = (new_url[0].split(' '))
        for i in a_list:
            if len(i) > 3:
                url_list.append(i)
                allowed_domains.append(i.replace('a@b','.'))
        print(url_list)
    except:
        pass

    def start_requests(self):
        url='http://%s'% str(self.url_list[-1]).split('\'')[1].replace('a@b','.')
        yield scrapy.Request(url,callback=self.parse)

    def get_list(self,response):
        print(response)

    def parse(self, response):
        html=response.body.decode('utf8')
        base_url=re.findall('<a href="(.*?)" id="item2">最新视频</a>', html)[0]
        for i in range(1,3):
            url = '%s%d/' % (base_url, i)
            res=requests.get(url).content.decode('utf8')
            html = etree.HTML(res)
            # print(type(html))
            res = html.xpath('//*[@id="list_videos_latest_videos_list_items"]/div/a')
            # print(res)
            for i in res:
                vip = i.xpath('./div[@class="img"]/span[@class="line-premium"]/span/img/@title')
                if not len(vip)>0:
                    href = i.xpath('./@href')[0]
                    name = i.xpath('./@title')[0]
                    img = i.xpath('./div[@class="img"]/img/@data-original')[0]
                    duration = i.xpath('./div[@class="wrap"]/div[@class="duration"]/text()')[0]
                    # print(duration)
                    yield scrapy.Request(url=href,callback=self.get_detail,dont_filter=True,meta={'name':name,'img':img,'duration':duration})

    def get_detail(self,response):
            res=response.body.decode('utf8')
            # print(res)
            # time.sleep(0.1)
            try:
                playurl=re.findall('" src="(.*?)" frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe',res)[0]
                item=MovieItem()
                item['d_playurl']=playurl
                item['d_pic']=response.meta.get('img')
                item['d_remarks']=response.meta.get('duration')
                item['d_name']=response.meta.get('name')
                item['d_type']=18
                item['d_playfrom']='m3u8'
                yield item
            except:
                print('失败')
