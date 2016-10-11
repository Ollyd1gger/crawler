# -*- coding: utf-8 -*-
import urlparse

import scrapy

from items import BitchstormItem

BASE_URL="http://www.harikadiziler.com/"
class BitchStormXPath(scrapy.Spider):
    name = 'bitchstorm'
    start_urls = [
        'http://www.harikadiziler.com/yabanci-dizi-bolumleri/',
    ]

    def parse(self, response):
        global a
        a =response.xpath('//div[@class="bolumler"]')
        global abuzer
        for abuzer in a.xpath('.//a/@href').extract():
            print abuzer
            global ziyver
            ziyver = "%s%s" %(BASE_URL,abuzer)
            yield scrapy.Request(urlparse.urljoin(BASE_URL,abuzer),callback=self.parse2)

    def parse2(self,response):
        print "yarrroli...%s" %response.meta
        if 'page' in response.meta:
            page = response.meta['page']
        else:
            page = 1

        d= response.xpath('//div[@class="video-izle"]/iframe').extract()

        x = page
        for line in d:
            zayteam = BitchstormItem()
            zibunkavayye= line
            print zibunkavayye
            if zibunkavayye == "":
                break;

            zayteam['href'] = zibunkavayye
            zayteam['text'] = response.xpath("//header[@class='video-baslik']/p/i/text()").extract()
            with open('log.txt', 'a') as f:
                f.write('{0}\n'.format(zibunkavayye))
            x+=1
            nexturlpage = "%s/%s" % (ziyver, x)
            print nexturlpage
            yield zayteam
            request = scrapy.Request(nexturlpage,callback=self.parse2)
            request.meta['page']=x
            yield request









