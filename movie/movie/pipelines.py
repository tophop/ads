# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import time


class MoviePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='host',
            port=3306,
            user='usr',
            password='pwd',
            db='db',
            charset='utf8'
        )

        self.conn2=pymysql.connect(
            host='host',
            port=3306,
            user='usr',
            password='pwd',
            db='db',
            charset='utf8'
        )

        self.conn_list=[self.conn,self.conn2]

        # self.cursor.execute('drop table if EXISTS douban')
        # sql = 'create table if not exists douban(id int(10)  NOT NULL AUTO_INCREMENT PRIMARY KEY,name varchar(50),comment varchar(400))'
        # self.cursor.execute(sql)

    def process_item(self, item, spider):
        for i in self.conn_list:
            self.cursor = i.cursor()
            try:
                d_playurl=item['d_playurl']
                d_pic=item['d_pic']
                d_remarks=item['d_remarks']
                d_name=item['d_name']
                d_type=item['d_type']
                d_playfrom=item['d_playfrom']
                d_addtime=time.mktime(time.localtime())
                d_time=d_addtime
                # sql = 'INSERT INTO mac_art (a_name,a_type,a_content) VALUES (%s,%d,%s)' %(item['name'],5,item['content'])'
                # sql="INSERT INTO shmwl_wenshushu_.mac_art (a_name,a_type,a_content) VALUES ({},'5',{})".format(a,b)
                sql='INSERT INTO mac_vod (d_name,d_playurl,d_pic,d_remarks,d_type,d_playfrom,d_addtime,d_time) VALUES ("%s","%s","%s","%s",%s,"%s","%s","%s");'%(d_name,d_playurl,d_pic,d_remarks,d_type,d_playfrom,d_addtime,d_time)

                self.cursor.execute(sql)
                print(item)
                # self.conn.commit()
                print('成功')
            except Exception as e:
                print(e)
                print('失败')
            self.cursor.close()

    def close_spider(self, spider):
        self.conn.close()