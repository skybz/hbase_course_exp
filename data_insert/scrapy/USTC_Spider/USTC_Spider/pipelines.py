# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class UstcSpiderPipeline:
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(dict(item))
        return item

    def close_spider(self, spider):
        with open('merged_output.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False)
