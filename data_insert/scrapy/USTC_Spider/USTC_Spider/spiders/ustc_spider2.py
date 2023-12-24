# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider2'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['https://www.teach.ustc.edu.cn/download/all']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        documents = response.xpath('//ul[@class="article-list with-tag download-list"]/li')
        for document in documents:
            title = document.xpath('.//span[@class="post"]/a/text()').get()
            link = document.xpath('.//span[@class="post"]/a/@href').get()
            publish_date = document.xpath('.//span[@class="date"]/text()').get()

            yield {
                'title': title,
                'link': response.urljoin(link),
                'publish_date': publish_date,
            }

        # 提取下一页链接并递归调用parse方法
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        
        if next_page != "javascript:void(0);" and self.page_count < 3:
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse)
