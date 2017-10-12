#-*-coding:utf-8 -*-
import sys
import requests
from lxml import etree

from mypipeline.Mysqlsave import MysqlPipeline
import urlparse
from fake_useragent import UserAgent
import re

reload(sys)
sys.setdefaultencoding("utf-8")

a = MysqlPipeline()

url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000%2C020000%2C030200%2C040000&keyword=python%20&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
ua = UserAgent()
headers = {
    "User-Agent": ua.random,
}

def get_html(url):
    kwargs = {}
    response = requests.get(url, headers=headers)
    html = response.content
    kwargs["url"] = url
    response = etree.HTML(html)
    kwargs["response"] = response
    return kwargs

# 的到所有页的url
i = 0
def parse_html(**kwargs):
    url = kwargs["url"]
    response = kwargs["response"]
    next_page = response.xpath("//li[@class='bk'][2]/a/@href")[0]
    global i
    i +=1
    print i
    if i == 100:
        print '防止递归, 栈溢出, 只爬去 递归 100 次 !'
        return
    if next_page:
        url_page = urlparse.urljoin(url, next_page)
        # print url_page
        kwargs = get_html(url_page)
        n = parse_datil(**kwargs)
        kwargs = {
            "url": next_page,
            "response": response,
        }
        print '-'*12

        return parse_html(**kwargs)

    else:
        print '已经到达最后一页'


# 解析详情页
def parse_datil(**kwargs):
    url = kwargs["url"]
    response = kwargs["response"]
    div_list = response.xpath("//div[@class='dw_table']/div[@class='el']")
    for div in div_list:
        zhi_wei = div.xpath("p/span/a/text()")[0].strip()
        # print zhi_wei
        gong_si = div.xpath("span[@class='t2']/a/text()")[0].strip()
        # print gong_si
        di_dian = div.xpath("span[@class='t3']/text()")[0].strip()
        # print di_dian
        gong_zi = div.xpath("span[@class='t4']/text()")
        if gong_zi:
            gong_zi = gong_zi[0].strip()
            args = parse_gong_zi(gong_zi)
            args = list(args)
            print args, type(args)
            if len(args) != None:
                ri_qi = div.xpath("span[@class='t5']/text()")[0].strip()
                print ri_qi
                result = [zhi_wei, gong_si, di_dian, ri_qi]
                result.append(args[0][0])
                result.append(args[0][1])
                print len(result), result
                a.save(result)
                print '保存成功!'
        else:
            gong_zi =  u"面议"



def parse_gong_zi(gong_zi):
    if gong_zi == u"面议":
        pass
    parrent = re.compile(r"[万千/月-]", re.S)
    result = parrent.search(gong_zi)
    many_max, many_min = 0, 0
    if result:
        if u"年" in gong_zi:
            result = gong_zi.replace(u"万/年", "").split("-")
            many_min = float(result[0]) * 10000 / 24
            many_max = float(result[1]) * 10000 /24
        elif u"万" in gong_zi:
            result = gong_zi.replace(u"万/月","").split("-")
            many_min = float(result[0]) * 10000
            many_max = float(result[1]) * 10000
        elif u"千" in gong_zi:
            result = gong_zi.replace(u"千/月", "").split("-")
            many_min = float(result[0]) * 1000
            many_max = float(result[1]) * 1000
        args =[str(many_min), str(many_max)]
        # print args
        yield args

def start(url):

    kwargs = get_html(url)
    parse_html(**kwargs)



if __name__ == '__main__':
    # url = "http://www.baidu.com"
    url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000%2C020000%2C030200%2C040000&keyword=python%20&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
    start(url)
    # kwargs = get_html(url)
    # parse_html(**kwargs)
