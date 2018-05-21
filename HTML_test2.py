# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 16:03
# @Author  : Simy Yan
# @File    : HTML_test.py
# @Software: PyCharm

from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request
import re


class MyHTMLParser(HTMLParser):
    a_t0 = False
    a_t1 = False
    a_t2 = False
    a_t3 = False
    a_t4 = False
    hightem=[]
    lowtem=[]

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

        if tag=="a"and _attr(attrs, 'href')=="http://bj.weather.com.cn":
            self.a_t0 = True
        elif tag=="h1":
            self.a_t1 = True
        elif tag=="p" and _attr(attrs, 'class')=="wea":
            self.a_t2 = True
        elif tag=='span':
            self.a_t3 = True
        elif tag=='i':
            self.a_t4 = True


    def handle_data(self, data):
        if self.a_t0 is True:
            self.information.append(dict(城市=data))
        elif self.a_t1 is True:
            if re.match(r'^\d{2}日\S+', data):
                self.information.append(dict(日期=data))    #list.append 添加在末尾，该list为多个dict集合
        elif self.a_t2 is True:
            self.information.append(dict(天气=data))
        elif self.a_t3 is True:
            if re.match(r'^\d{2}\S$', data):
                self.information.append(dict(最高温=data))
        elif self.a_t4 is True:
            if re.match(r'^\d{2}\S{1}$', data):
                self.information.append(dict(最低温=data))

    def handle_endtag(self, tag):
        if tag == 'a':
            self.a_t0 = False
        elif tag == "h1":
            self.a_t1 = False
        elif tag =="p":
            self.a_t2 = False
        elif tag =="span":
            self.a_t3 = False
        elif tag =="i":
            self.a_t4 = False

def parseHTML(html_str):
    parser = MyHTMLParser()
    parser.feed(html_str)  #接受HTML并解析
    for i, val in enumerate(parser.information):  #enumerate将list变为索引-元素对。遍历打印value
        i +=  1
        print(val)
        if (i-1)%4==0:
            print('--------------------------------------------')


URL = 'http://www.weather.com.cn/weather/101010100.shtml'
with request.urlopen(URL, timeout=10) as f: # 收集页面信息 timeout：设置网站的访问超时时间
    data = f.read()

parseHTML(data.decode('utf-8'))  #data的数据格式为bytes类型，需要decode（）解码，转换成str类型。
# 将收到的信息解码，并传给parseHTML()调用
