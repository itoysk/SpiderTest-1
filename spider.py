# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import thread
import time

class MySpider:
    def __init__(self):
        self.page = 1
        self.contents = []
        self.enable = False

    def GetContentByPage(self,page):
        myUrl = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(myUrl,headers=headers)
        myResponse = urllib2.urlopen(req)
        tempHtmlText = myResponse.read()
        htmlText = tempHtmlText.decode("utf-8")

        myItems = re.findall(r'<div class="content">(.*?)</div>',htmlText,re.S)
        items = []
        for item in myItems:
            items.append([item.replace("\n", "")])
        return items

    def LoadPage(self):
        while self.enable:
            if len(self.contents) < 2:
                try:
                    tempContents = self.GetContentByPage(str(self.page))
                    self.page += 1
                    self.contents.append(tempContents)
                except:
                    print u'无法链接'
            else:
                time.sleep(1)

    def Show(self,currentContents,page):
        for items in currentContents:
            print "第%d页" % page,items[0]
            myInput = raw_input()
            if myInput == "quit":
                self.enable = False
                break

    def Start(self):
        self.enable = True
        page = self.page
        print  '正在加载中'

        thread.start_new(self.LoadPage,())

        while self.enable:
            if self.contents:
                currentContents = self.contents[0]
                del self.contents[0]
                self.Show(currentContents,page)
                page += 1

#开始
q = raw_input('就输入回车键开始获取：')
mySpider = MySpider()
mySpider.Start()