# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider4'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['https://finance.ustc.edu.cn/xzzx/list.psp']
    page_count = 1

    def parse(self, response):
        # 提取文档信息
        documents = response.css('ul.news_list li')
        for document in documents:
            title = document.css('span.news_title a::text').get()
            link = document.css('span.news_title a::attr(href)').get()
            publish_date = document.css('span.news_meta::text').get()

            # # 如果链接是以.htm结尾的，就发起请求获取对应页面的内容
            if link.endswith('.htm'):
                link = link.replace('.htm', '.psp')
                
            if link.endswith('.psp'):
                yield scrapy.Request(response.urljoin(link), callback=self.parse_html_document)
            
            else :
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                    'publish_date': publish_date,
                    }

        # 提取下一页链接并递归调用parse方法
        next_page = response.css('li.page_nav a.next::attr(href)').get()
        next_page = next_page.replace('.htm', '.psp')
        
        if next_page != "javascript:void(0);" and self.page_count < 3:
            self.page_count += 1
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_html_document(self, response):
        # 处理点击链接后打开的页面内容
        article = response.css('.article')
        title = article.css('h1.arti_title::text').get()
        publish_date = article.css('p.arti_metas span.arti_update::text').get()
        link = response.css('div.read div.wp_articlecontent div.wp_pdf_player::attr(pdfsrc)').get()
        if (link is None):
            link = response.css('div.entry div.read div.wp_articlecontent p a::attr(href)').get()

        yield {
            'title': title,
            'link': response.urljoin(link),
            'publish_date': publish_date,  
        }