# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider6'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['http://ispc.ustc.edu.cn/6299/list.htm','http://ispc.ustc.edu.cn/6298/list.htm']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        documents = response.css('div#wp_news_w6 li')
        for document in documents:
            title = document.css('a::attr(title)').get()
            link = document.css('a::attr(href)').get()
            publish_date = document.css('span.time::text').get()
                
            if link.endswith('.htm'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_html_document)
            
            else :
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'publish_date': publish_date,
                    }

        # 提取下一页链接并递归调用parse方法
        next_page = response.css('script:contains("var wp_pagingbarJson")::text').get()
        
        if next_page != "javascript:void(0);" and self.page_count < 3:
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_html_document(self, response):
        # 处理点击链接后打开的页面内容
        title = response.css('span[frag="窗口5"]::text').get()
        link = response.css('div.wp_articlecontent a::attr(href)').get()
        # if link is  None:
        #     link = response.css('div.wp_articlecontent a.appendix::attr(href)').get()
        date = response.css('span[frag="窗口6"]::text').get()

        if (link):
            yield {
                'title': title.strip(),
                'link': response.urljoin(link),
                'publish_date': date.strip(),
            }