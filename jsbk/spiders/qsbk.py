# -*- coding: utf-8 -*-
import scrapy
from jsbk.items import JsbkItem
class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"
    def parse(self, response):
        # response的类型是scrapy.http.response.html.HtmlResponse
        duanzidivs = response.xpath(".//div[@class='col1 old-style-col1']/div ")
        for duanzidiv in duanzidivs:
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = JsbkItem(author=author, content=content)
            yield item
        next_url = response.xpath(".//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url, callback=self.parse)
