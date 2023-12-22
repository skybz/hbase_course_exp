# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider7'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['http://zhb.ustc.edu.cn/18534/list.htm']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        articles = response.css('ul.wp_article_list li.list_item')
        for article in articles:
            link = article.css('div.fields.pr_fields span.Article_Title a::attr(href)').get()
            title = article.css('div.fields.pr_fields span.Article_Title a::text').get()
            publish_date = article.css('div.fields.ex_fields span.Article_PublishDate::text').get()

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
        title = response.css('h1.arti_title::text').get()
        date = response.css('p.arti_metas span.arti_update::text').get()
        link = response.css('div.read div.wp_articlecontent a::attr(href)').get()

        yield {
            'title': title.strip(),
            'link': response.urljoin(link),
            'publish_date': date.strip(),
        }