# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [(x['path'], x['url']) for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

import os
import errno
import shutil
from scrapy.utils.project import get_project_settings

class MakeHtmlPipeline(object):

    def my_mkdir(self, dirpath):
        # make the dir
        try:
            os.makedirs(dirpath)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def process_item(self, item, spider):

        dirname = os.getcwd() + "\\lingzhuzi\\" + item['title']
        self.my_mkdir(dirname)
        filedir = dirname + "\\" + "image_files" + "\\"
        imagedir = filedir + "\\" + "full"
        self.my_mkdir(imagedir)

        for imgpath in item['image_paths']:
            src = get_project_settings().get('IMAGES_STORE') + "/" + imgpath[0]
            des = filedir + "/" + imgpath[0]

            shutil.copy(src, des)

            htmlimage = "image_files" + "/" + imgpath[0]
            print htmlimage
            item['htmlbody'] = item['htmlbody'].replace(imgpath[1].encode('gbk'), htmlimage.encode('gbk'))

        with open(dirname + "\\" + item['title'] + ".html", 'w') as htmlfile:
           htmlfile.write(item['htmlbody'])
        item['htmlbody'] = "";
        return item
