# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [(x['path'], x['url']) for ok, x in results if (ok and ((r'images/post/smile/default' not in x['url'])))]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

import os
import errno
import shutil
import json
import MySQLdb
import re
from scrapy.utils.project import get_project_settings

class SaveDBPipeline(object):
    def process_item(self, item, spider):
        response = item['response']
        links = response.xpath('//div[contains(@class,"f14")]/font/span/span')
        links2 = response.xpath('//div[contains(@class,"f14")]/font/span')
        #f = "</span><br/>图2，此图摄于2014年，当时坐船游西湖，远视诸山，只嫌雾霾不清，但仿佛见此处星体端正，是九星中之吉星，知其间应有佳壤，但想一是景区之内，二是没时间去探访，远远看一下就算了，当然此时未意识到这里在【地理人子须知】中有记载。<br/><br/<span"
        #p1 =  r'</span>(.*?<span|.*?</span>){1}'
        #p1 =  r'</span>.*?</?span'
        p1 =  r'</span>(.*?)</?span'
        pattern1 = re.compile(p1)

        content_list = list()
        for link in links2:

            strlink = (link.extract())
            #print strlink
            find = pattern1.findall(strlink)
            # if find:
            #     print ''.join(find)
            # else:
            #     print 'not match'
            for fi in find:
                fi = fi.replace('<br>', '')
                fi = fi.replace('</br>', '')
                content_list.append(fi)
        article_contents = [{'img':link.xpath('img/@src').extract(), 'content': link.xpath('b/text()').extract_first().encode('utf-8')} for link in links]

        # for link in links:
        #     print ''.join(link.xpath('b/text()').extract())
        contenttemp = ''
        for content in article_contents:
            contenttemp = content['content']
            content['content'] = content['content'];

        count = len(article_contents) < len(content_list) and len(article_contents) or len(content_list)
        for i in range(0, count):
            #article_contents[i]['content'] += ('{#br#}' + content_list[i])
            pass
        db = MySQLdb.connect("localhost", "root", "", "samp_db")

        article_content_str = json.dumps(article_contents, ensure_ascii=False)

        print article_content_str
        cursor = db.cursor()
        cursor.execute("SET NAMES utf8")
        # sql = 'INSERT INTO `article`'
        # sql = sql + '(`article_title`,`article_content`)'
        # sql = sql + 'VALUES(`' + ''.join(item['title']) + '`,`' + article_content_str + '`);'

        sql = "INSERT INTO article \
              (`article_title`,`article_content`) \
              VALUES('%s', '%s');" % (item['title'], article_content_str.encode('utf-8'))

        print 'sql:' + sql
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

        sql = "SELECT * FROM article \
               WHERE article_id = '%d'" % (178)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if results:
            for row in results:
                print "id = %s, title=%s, content =%s\n" % \
                      (row[0], row[1], row[2])
                jsondata = json.loads(row[2], encoding="utf-8")
                print ''.join(jsondata[2]['content'])
            db.close()
        return item

class MakeHtmlPipeline(object):

    def my_mkdir(self, dirpath):
        # make the dir
        try:
            os.makedirs(dirpath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def process_item(self, item, spider):
        dirname = os.path.join(os.getcwd(), "lingzhuzi")
        dirname = os.path.join(dirname, item['title'])
        #print dirname
        self.my_mkdir(dirname)
        filedir = os.path.join(dirname, "image_files" )
        imagedir = filedir
        self.my_mkdir(imagedir)
        #<base id="headbase" href="http://www.ok88ok88.com/" />
        needreplace = '<base id="headbase" href="http://www.ok88ok88.com/" />'
        replacebase = '<base href=".">'
        item['htmlbody'] = item['htmlbody'].replace(needreplace.encode('gbk'), replacebase.encode('gbk'))
        for imgpath in item['image_paths']:
            src = os.path.join(get_project_settings().get('IMAGES_STORE'), imgpath[0])
            des = os.path.join(filedir, imgpath[0].split('/')[1])
            shutil.copy(src, des)
            htmlimage = os.path.join("image_files", imgpath[0].split('/')[1])
            item['htmlbody'] = item['htmlbody'].replace(imgpath[1].encode('gbk'), htmlimage.encode('gbk'))
        filepath = os.path.join(dirname,  item['title'] + ".html")
        with open(filepath, 'w') as htmlfile:
           htmlfile.write(item['htmlbody'])
        item['htmlbody'] = ""
        return item
