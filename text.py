# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

#慕课爬虫类
class IMooc:

    def __init__(self,baseUrl):
        self.baseUrl = baseUrl
        
    def getPage(self,viewId):
        try:
            headers = {  
               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
            }  
            url = self.baseUrl + str(viewId)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接mooc失败，错误原因",e.reason
                return None
    
    def getContent(self,pageIndex):
        try:
            headers = {  
               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
            }  
            url='http://www.mooc.cn/tag/classic/page/'+ str(pageIndex)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接mooc失败，错误原因",e.reason
                return None
                
    def getTitle(self,page):
        pattern = re.compile('<title>(.*?)</title>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getBrief(self,page):
        pattern = re.compile('<div class="course-excerpt">.*?>(.*?)</p>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getTime(self,page):
        pattern = re.compile('<div class="coursetime">(.*?)</div>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getping(self,page):
        pattern = re.compile('<em class="join-strong-gw join-strong-bg">(.*?)</em>',re.S)
        result = re.search(pattern,page)
        print result
        if result:
            return result.group(1).strip()
        else:
            return None

    def getViewsId(self,page):
        pattern = re.compile('<h1 class="courselist-title".*?<a target="_blank" href="http://www.mooc.cn/course/(.*?)"',re.S)
        result = re.findall(pattern,page)
        return result

    

    def start(self):
        indexPage = self.getContent(1)
        file = open("imooc.txt","w+")
        try:
            for i in range(1,3):
                indexPage = self.getContent(i)
                ViewsId = self.getViewsId(indexPage)
                for item in ViewsId:
                    page = self.getPage(item)
                    title = self.getTitle(page)
                    file.write('\n'+'课程题目：' + title)
                    brief = self.getBrief(page)
                    file.write('\n'+'课程介绍：' + brief)
                    time = self.getTime(page)
                    file.write('\n'+ time)
                    # ping = self.getping(page)
                    # file.write('\n'+'课程介绍：' + ping)
                    # outline = self.getOutline(page)
                    # file.write('\n'+'课程提纲：' + '\n')
                    # for item in outline:
                    #     file.write(item[0] + '\n')
                    #     file.write(item[1] + '\n')
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"
        
baseUrl = "http://www.mooc.cn/course/"
imooc = IMooc(baseUrl)
imooc.start()