# -*- coding: utf-8 -*-
# @Time    : 2018/5/12 16:03
# @Author  : john fan
# @Email   : jianlongfan@gmail.com
# @File    : ex_HTMLPASER_2.py
# @Software: PyCharm

from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request
import re


class MyHTMLParser(HTMLParser):
    a_t1 = False
    a_t2 = False
    a_t3 = False
    def __init__(self):
        HTMLParser.__init__(self)
        self.information = []
        self.information_all = {}


    def handle_starttag(self, tag, attrs):  #遇到<xxx>首先运行handle_starttag，然后handle_data，
                                            # 遇到</xxx>运行handle_endtag，为一条完整tag
        def _attr(attrlist, attrname):      #获取 <span class="event-location">Heidelberg, Germany</span>
            for attr in attrlist:           #attr[0]='class'，attr[1]="event-location"
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag=="time":
            self.a_t1 = True
        elif tag=="span" and _attr(attrs, 'class')=="event-location":
            self.a_t2 = True
        elif tag=="h3" and _attr(attrs, 'class')=="event-title":
            self.a_t3 = True


    def handle_data(self, data):
        if self.a_t1 is True:
            if re.match(r'^\s\d{4}', data):
                self.information.append(dict(year=data))    #list.append 添加在末尾，该list为多个dict集合
            else:
                self.information.append(dict(day=data))
        elif self.a_t2 is True:
            self.information.append(dict(event_location=data))
        elif self.a_t3 is True:
            self.information.append(dict(event_title=data))


    def handle_endtag(self, tag):
        if tag == "time":
            self.a_t1 = False
        elif tag =="span":
            self.a_t2 = False
        elif tag == "h3":
            self.a_t3 = False



def parseHTML(html_str):
    parser = MyHTMLParser()
    parser.feed(html_str)  #接受HTML并解析
    for i, val in enumerate(parser.information):  #enumerate将list变为索引-元素对。遍历打印value
        i +=  1
        print(val)
        if i%4==0:
            print('--------------------------------------------')


URL = 'https://www.python.org/events/python-events/'
with request.urlopen(URL, timeout=4) as f: # 收集页面信息 timeout：设置网站的访问超时时间
    data = f.read()

parseHTML(data.decode('utf-8'))  #data的数据格式为bytes类型，需要decode（）解码，转换成str类型。
# 将收到的信息解码，并传给parseHTML()调用
