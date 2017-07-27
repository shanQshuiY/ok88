import scrapy

class Ok88Spider(scrapy.Spider):

    name = "ok88spider"
    allowed_domains = ["ok88ok88.com"]
    start_urls = ["http://www.ok88ok88.com/read.php?tid=22159"]

    def parse(self, response):

        #a[contains(@href, "image")]
        #all_links = response.xpath('//a/@href')
        #driver.find_element_by_xpath("//a[contains(@id,'url_165')]")
        all_links = response.xpath('//a[contains(@id,"url_")]/text()')

        for link in all_links:
            #print link.extract()
            if  link.re(r'http://w{0,3}\.?ok88ok88.com/read\.php\?tid=\d{2,5}$') is not None:
                yield scrapy.Request(link.extract(), callback=self.parse_dir_contents)
            #print link.re(r"http://www.ok88ok88.com/read.php?tid=.*")
            # if link.re(r"http://www.ok88ok88.com/read.php?tid=.*"):
            #     print link.extract()
            # else:
            #     print "Not a needed page!"
    def parse_dir_contents(self, response):
        print "get url" + response.url
