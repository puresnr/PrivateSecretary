#! /usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import random
import re
import datetime
from bs4 import BeautifulSoup


#这个网址默认请求只返回7天的数据，因此一星期执行一次的话，下星期的这天凌晨的比赛可能会错过.
url = "http://www.dongqiudi.com/match/fetch_new?tab=null&date=%s&scroll_times=1&tz=-8" % (datetime.datetime.now().strftime("%Y-%m-%d"))
host = "www.dongqiudi.com"
referer = "http://www.dongqiudi.com/match"
my_team = [u'北京中赫国安', u'阿森纳', u'拜仁慕尼黑', u'中国', u'德国']



''' 
#@获取403禁止访问的网页 
'''  
my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",  
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",  
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"  
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]
def get_content(url, host, referer):  
    req=urllib.request.Request(url)  
    req.add_header("User-Agent",random.choice(my_headers))  
    req.add_header("Host", host)  
    req.add_header("Referer", referer)
    req.add_header("GET",url)  
    content=urllib.request.urlopen(req).read()  
    return content

 
week_day = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
match_text = get_content(url, host, referer).decode('unicode-escape')
now = datetime.datetime.now()
for i in range(1, 8):
    cur_day = now + datetime.timedelta(days = i - 1)
    next_day = now + datetime.timedelta(days = i)
    day_text = match_text[match_text.find("<th colspan=\"6\">%s" % (cur_day.strftime('%Y-%m-%d'))) : match_text.find("<th colspan=\"6\">%s" % (next_day.strftime('%Y-%m-%d')))]
    split_text = BeautifulSoup(day_text, "html.parser").get_text("", strip = True).split("<\\/tr>")
    is_print = False
    for text in split_text:
        for team in my_team:
            if text.find(team) != -1:
                if is_print == False:
                    is_print = True
                    print('**********比赛日: ' + cur_day.strftime('%Y-%m-%d') + ' ' + week_day[cur_day.weekday()] + '**********')
                match_info = re.sub(r'[\n<>\\/tda]', " ", text).split()
                print("开赛时间: %s   赛事名称: %s\n%s %s %s\n" % (match_info[0], match_info[1], match_info[2], match_info[3], match_info[4]))
input()

#import sys
#sys.setrecursionlimit(1000000)   递归过长时出错时，可以设置一下限制
                
#with open ('target.txt', 'w', encoding='utf-8') as fw:
#   fw.write(text)
#with open("test.html", "w") as f:    
#    f.write(get_content(url, host, referer).decode('unicode-escape'))
