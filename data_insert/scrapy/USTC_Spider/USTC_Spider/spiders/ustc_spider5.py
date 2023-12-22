# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider5'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['https://bwc.ustc.edu.cn/5655/list.htm']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        documents = response.css('ul.list-group li.list-group-item')
        for document in documents:
            title = document.css('a::attr(title)').get()
            link = document.css('a::attr(href)').get()
            publish_date = document.css('span.badge.hidden-xs::text').get()
                
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
        title = response.css('div.heading-section h2 span::text').get()
        link = response.css('div.wp_articlecontent p a::attr(href)').get()
        if link is  None:
            link = response.css('div.wp_articlecontent a.appendix::attr(href)').get()
        date = response.css('div.heading-section h4 span::text').get()

        yield {
            'title': title.strip(),
            'link': response.urljoin(link),
            'publish_date': date.strip(),
        }