# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider8'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['http://young.ustc.edu.cn/15056/list.htm']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        items = response.css('ul.text-ul li.text-li')
        for item in items:
            publish_date = item.css('i::text').get()
            link = item.css('a::attr(href)').get()
            title = item.css('span a::attr(title)').get()

            if link.endswith('.htm'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_html_document)
            
            else :
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'publish_date': publish_date,
                    }

        # 提取下一页链接并递归调用parse方法
        next_page = response.css('li.page_nav a.next::attr(href)').get()
        
        if next_page != "javascript:void(0);" and self.page_count < 3:
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_html_document(self, response):
        # 处理点击链接后打开的页面内容
        date = response.css('div.tb-wrap span:nth-child(1)::text').get()
        title = response.css('h1.ta-wrap::text').get()
        link = response.css('div.tc-wrap a::attr(href)').get()

        if (link):
            yield {
                'title': title.strip(),
                'link': response.urljoin(link),
                'publish_date': date.strip(),
            }