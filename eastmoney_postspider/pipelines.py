# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import os
import MySQLdb
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('output.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item


class SqlWriterPipeline(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="rfvtgbyhnujm", port=3306, db="eastmoney", charset="utf8")
            self.cursor = self.db.cursor()
        except:
            sys.stderr("Connect Failed")

    def process_item(self, item, spider):
        indexnum = 0
        if item['title']:
            for title in item['title']:
                code = item['code'][indexnum]
                writer = item['writer'][indexnum]
                read = item['writer'][indexnum]
                comment = item['writer'][indexnum]
                date = item['date'][indexnum]
                url = item['url'][indexnum]
                year = item['year'][indexnum]
                if int(year) == 2016:
                    param = (code, title, date, writer, read, comment, url)
                    sql_insert = "INSERT INTO posts (code,title,date,writer,read,comment,url) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    self.cursor.excute(sql_insert, param)
                indexnum = indexnum + 1
        else:
            raise DropItem(item)

        return item

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()
        sys.stdout("Closed")
