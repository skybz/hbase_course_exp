# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider(scrapy.Spider):
    name = 'ustc_spider3'
    allowed_domains = ['ustc.edu.cn']
    start_urls = ['https://physics.ustc.edu.cn/main.htm']
    page_count = 1

    def parse(self, response):
        # 使用XPath选择器提取连接
        links = response.xpath('//ul[@id="nav_i11"]/div/li/a/@href').extract()

        # 处理提取到的连接，可以输出或进一步处理
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_html)

    def parse_html(self, response):
        # 提取文档信息
        items = response.css('div[frag="窗口07"] h4 a')
        for item in items:
            link = item.css('::attr(href)').extract_first()
            title = item.css('::text').extract_first()
            # 日期设置为空
            publish_date = "null"

            # 如果链接是以.htm结尾的，就发起请求获取对应页面的内容
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
        next_page = response.xpath('//a[@class="next"]/@href').get()
        next_page = next_page.replace('.htm', '.psp')
        if next_page != "javascript:void(0);":
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_html_document(self, response):
        # 处理点击链接后打开的页面内容
        title = response.css('div.article-tit h1::text').get().strip()
        link = response.css('div.row-fluid div.wp_articlecontent div.wp_pdf_player::attr(pdfsrc)').get()

        # 日期设置为空
        publish_date = "null"

        yield {
            'title': title,
            'link': response.urljoin(link),
            'publish_date': publish_date,  
        }