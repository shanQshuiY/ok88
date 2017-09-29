# -*- coding: utf-8 -*-
import scrapy
from ok88.items import Ok88Item


class Ok88Spider(scrapy.Spider):

    name = "ok88spider"
    allowed_domains = ["ok88ok88.com"]
    start_urls = ["http://www.ok88ok88.com/read.php?tid=22159"]

    def parse(self, response):

        #all_links = response.xpath('//a[contains(@id,"url_")]/text()')
        #link = "http://www.ok88ok88.com/read.php?tid=98531&uid=1"
        all_links = response.xpath('//a[contains(@href,"95362")]/text()')
        for link in all_links:
            if link.re(r'http://w{0,3}\.?ok88ok88.com/read\.php\?tid=\d{2,5}$'):
                yield scrapy.Request(link.extract() + "&uid=1", callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = Ok88Item()
        #item['title'] = response.xpath('//meta[contains(@name,"keywords")]/@content').extract_first().encode('utf-8')
        item['title'] = response.xpath('//head/title/text()').extract_first().encode('utf-8').replace("- 龙行天下风水论坛 中国风水品牌论坛 最佳的风水交流学习平台 - Powered by PHPWind.net", "")
        links = response.xpath('//div[contains(@class,"f14")]//img/@src')
        urls = links.extract()
        newurls = [ url for url in urls if not 'images/post/smile/default/' in url]
        item['image_urls'] = newurls
        item['htmlbody'] = response.body
        item['response'] = response
        yield item

