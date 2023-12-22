# -*- coding: utf-8 -*-
import scrapy

class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider1'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['http://sds.ustc.edu.cn/15413/list.htm']

    def parse(self, response):
        # 提取文档信息
        documents = response.xpath('//ul[@class="wp_article_list"]/li')
        for document in documents:
            title = document.xpath('.//span[@class="Article_Title"]/a/text()').get()
            link = document.xpath('.//span[@class="Article_Title"]/a/@href').get()
            publish_date = document.xpath('.//span[@class="Article_PublishDate"]/text()').get()

            # 如果链接是以.htm结尾的，就发起请求获取对应页面的内容
            if link.endswith('.htm'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_html_document)

            else:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'publish_date': publish_date,
                }

        # 提取下一页链接并递归调用parse方法
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page != "javascript:void(0);":
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_html_document(self, response):
        # 处理点击链接后打开的页面内容
        title = response.xpath('//h1[@class="arti_title"]/text()').get()
        link = response.xpath('//div[@class="wp_pdf_player"]/@pdfsrc').get()
        if link is None :
            link = response.xpath("//div[@class='entry']//a/@href").get()
        publish_date = response.xpath('//span[@class="arti_update"]/text()').get()[5:]

        yield{
            'title': title,
            'link': response.urljoin(link),
            'publish_date': publish_date,
        }
