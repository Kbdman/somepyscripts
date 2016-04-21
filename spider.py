# coding=utf-8
# 目前的功能是可以去51job上去抓点南京地区的c++的职位列表,写入名为data.csv文件中
# search_from_51_keywords('c++', '南京', sn)中的c++可以替换成其他关键字
# 第二个参数是城市，目前只支持南京，'南京'，如果想支持其他城市，需要完善下search_from_51_keywords函数中的变量dic 
import urllib
import requests
import json
import re
import string
from sgmllib import SGMLParser


def get_str_between(str, chara, charb):
    indexa = str.find(chara)
    indexb = str.find(charb)
    if indexa == -1:
        return ''
    if indexb == -1:
        return ''
    return str[indexa + len(chara):indexb]


class analyzer51_getpagecount(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_span = ""
        self.count = ''

    def start_span(self, attrs):
        self.is_span = 1

    def end_span(self):
        self.is_span = ""

    def handle_data(self, text):
        if self.is_span == 1:
            tmp = get_str_between(text, '共', '页')
            if tmp != '':
                self.count = int(tmp)


class analyzer51_getjobs(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.in_result_list = 0
        self.tmp = []
        self.in_t1 = 0
        self.in_a = 0
        self.in_el = 0
        self.url = ''
        self._index=-1
        self.reslist=[];
        self.ti=''
    def start_p(self, attrs):
        self._index = -1
        self.in_t1 = 0
        if self.in_result_list > 0:
            ca = [v for k, v in attrs if k == 'class']
            if (ca.__len__()>0) and (ca[0] == 't1'):
                self.in_t1 = 1
                self._index=0
    def end_p(self):
        self.in_t1 = 0
        self._index=-1

    def start_a(self, attrs):
        if self.in_el==0:
            return
        self.in_a = 1
        url = [v for k, v in attrs if k == 'href']
        if url.__len__()>0:
            self.url=url[0]
            ti=[v for k, v in attrs if k == 'title']
            if url.__len__() > 0:
                self.ti=ti[0]

    def end_a(self):
        self.in_a = 0
        self.ti=''
        self.url=''

    def start_span(self, attrs):
        cla = [v for k, v in attrs if k == 'class']
        if (self.in_result_list > 0) and cla:
            clas=['t2','t3','t4','t5']
            if cla.__len__() > 0:
                for i in range(0,4):
                    if clas[i]==cla[0]:
                        self._index=i+1


    def end_span(self):
        self._index=-1

    def start_div(self, attrs):
        self._index = -1;
        name = [v for k, v in attrs if k == 'id']
        if (name.__len__()>0 and name[0] == 'resultList') or (self.in_result_list != 0):
            self.in_result_list += 1
        cla = [v for k, v in attrs if k == 'class']
        if (self.in_result_list > 0) and cla:
            if cla.__len__()>0 and cla[0] == 'el':
                self.in_el=1
                self.tmp = ['','','','','','','']
                self._index=-1;

    def end_div(self):
        if self.in_result_list > 0:
            self.in_result_list -= 1
        self.in_el = 0
        self._index=-1

    def handle_data(self, text):
        if strtrip(text)=='':
            return
        txt=text
        if self.in_el == 1:
            if self.in_a == 1:
                self.tmp[self._index+5] = self.url
                txt=self.ti
            if self._index>-1 :
                self.tmp[self._index]=(strtrip(txt)).replace(',','.')
            if self._index==4:
                self.reslist.append(self.tmp)


def getPageCount(html51):
    pagecount = re.findall('\<span class=\"td\"\>共.*页', html51)[0];
    print pagecount


def strtrip(str):
    str = str.replace('\n', '');
    str = str.replace('\t', '');
    str = str.replace('\r', '');
    str = str.replace(' ', '');
    return str


def getHtml(url, sn):
    # 先获取总页数
    # 请求所有页数
    page = sn.get(url)
    # html = strtrip(page.content);
    return page.content.decode('gb2312').encode('utf8')


def search_from_51_keywords(key, area, sn):
    dic = {'南京': '070200'}
    url = "http://search.51job.com/jobsearch/search.html?fromJs=1"
    payload = {'keyword': key, 'btnJobarea': '', 'jobarea': dic[area]}
    n = sn.post(url, payload).content;
    r = re.findall('http:\/\/search.*=0', n)[0]
    return r


def get_jobs_from_51(url, sn,analyzer):
    con = sn.get(url).content.decode('gb2312').encode('utf-8');
    analyzer.feed(con);


sn = requests.session();
sn.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'})
url = search_from_51_keywords('c++', '南京', sn)
html = getHtml(url, sn)
pagecounter = analyzer51_getpagecount();
pagecounter.feed(html);
pagecount = pagecounter.count
urlend = url[url.find('.html'):]
urlbegin = url[0:url[0:url.find('.html')].rfind(',') + 1]
url = {};
output = open('data.csv', 'w');
an = analyzer51_getjobs()
for i in range(1, pagecount + 1):
    url[i] = urlbegin + str(i) + urlend
for i in url:
    get_jobs_from_51(url[i], sn, an)
for i in an.reslist:
    k=0
    for j in i:
        output.write(j)
        k+=1
        if k==7:
            output.write('\n')
        else:
            output.write(',')


