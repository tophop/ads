# -*- coding: utf-8 -*-
import re
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


class XihubSpider(scrapy.Spider):
    name = 'xihub'
    allowed_domains = ['x12.com']
    start_urls = ['http://x1212.com/']
    ua = get_ua()
    a = {'User-Agent': ua}

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        html = response.body.decode('utf8')
        infos = re.findall('<div class="col-xs-12 col-sm-6 col-md-3 col-lg-3">(.*?)<div class="caption">', html, re.S)
        for info in infos:
            name = re.findall('<a target="_blank" title="(.*?)" href=', info, re.S)[0]
            img = re.findall('original="(.*?)" data-load=', info, re.S)[0]
            duration = re.findall('<var class="duration">(.*?)</var>', info, re.S)[0]
            playurl = re.findall('<a target="_blank" title="(.*?)" href="(.*?.html)', info, re.S)[0][1]
            detail_url = self.start_urls[0] + playurl
            yield scrapy.Request(detail_url, callback=self.parse_playurl,
                                 meta={'name': name, 'img': img, 'duration': duration})

    def parse_playurl(self, response):
        res = response.body.decode('utf8')
        play_url = re.findall('allowfullscreen="true" src="(.*?);.*?" id="playIframe', res, re.S)[0]
        # src = "https://dadi-yun.com/share/b7b58836dc941cc4ba33d16dab6e3059"
        # id = "playIframe"
        # pass
        item = MovieItem()
        item['d_playurl'] = "%s%s?embed" % (self.start_urls[0],play_url.lstrip('/'))
        item['d_pic'] = response.meta.get('img')
        item['d_remarks'] = response.meta.get('duration')
        item['d_name'] = response.meta.get('name')
        item['d_type'] = 19
        item['d_playfrom'] = 'm3u8'
        yield item
