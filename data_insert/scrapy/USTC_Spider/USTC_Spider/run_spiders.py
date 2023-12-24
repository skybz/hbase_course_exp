# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class UstcSpiderSpider1(scrapy.Spider):
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

class UstcSpiderSpider2(scrapy.Spider):
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

class UstcSpiderSpider3(scrapy.Spider):
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

# -*- coding: utf-8 -*-
import scrapy


class UstcSpiderSpider4(scrapy.Spider):
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

class UstcSpiderSpider5(scrapy.Spider):
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

class UstcSpiderSpider6(scrapy.Spider):
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


class UstcSpiderSpider7(scrapy.Spider):
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


class UstcSpiderSpider8(scrapy.Spider):
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


def run_spiders():
    process = CrawlerProcess(get_project_settings())

    # 添加所有的 Spider 类到 CrawlerProcess
    process.crawl(UstcSpiderSpider1)
    process.crawl(UstcSpiderSpider2)
    process.crawl(UstcSpiderSpider3)
    process.crawl(UstcSpiderSpider4)
    process.crawl(UstcSpiderSpider5)
    process.crawl(UstcSpiderSpider6)
    process.crawl(UstcSpiderSpider7)
    process.crawl(UstcSpiderSpider8)

    # 启动爬虫
    process.start()

if __name__ == '__main__':
    run_spiders()