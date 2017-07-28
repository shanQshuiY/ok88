# -*- coding: gbk -*-
import scrapy
from ok88.items import Ok88Item


class Ok88Spider(scrapy.Spider):

    name = "ok88spider"
    allowed_domains = ["ok88ok88.com"]
    start_urls = ["http://www.ok88ok88.com/read.php?tid=22159"]

    def parse(self, response):

        all_links = response.xpath('//a[contains(@id,"url_")]/text()')
        link = "http://www.ok88ok88.com/read.php?tid=98531&uid=1"
        yield scrapy.Request(link, callback=self.parse_dir_contents)
        # for link in all_links:
        #     if link.re(r'http://w{0,3}\.?ok88ok88.com/read\.php\?tid=\d{2,5}$'):
        #         yield scrapy.Request(link.extract() + "&uid=1", callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        #print response.body.decode('gbk')
        item = Ok88Item()
        item['title'] = response.xpath('//meta[contains(@name,"keywords")]/@content').extract_first()
        links = response.xpath('//div[contains(@class,"tpc_content")]//img/@src')
        item['image_urls'] = links.extract()
        item['htmlbody'] = response.body.decode('gbk')

        yield item

