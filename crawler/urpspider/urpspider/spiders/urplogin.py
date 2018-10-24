# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import json
from ..items import classScheduleItem,userItem
from warehouse.models import user
class PachSpider(scrapy.Spider):                            #定义爬虫类，必须继承scrapy.Spider
    name = 'urplogin'                                           #设置爬虫名称
    allowed_domains = ['zhjw.scu.edu.cn']                  #爬取域名
    # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理
    logindata = {'j_username': '0', 'j_password': '0', 'j_captcha1': 'error'}
    usermsg = userItem()

    def __init__(self, logindata=None, *args, **kwargs):
        super(PachSpider, self).__init__(*args, **kwargs)
        self.logindata = json.loads(logindata)
    def start_requests(self):       #用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        self.usermsg['userID'] = str(self.logindata['j_username'])
        self.usermsg['userName'] = ""
        self.usermsg['userPassword']=str(self.logindata['j_password'])
        self.usermsg.save()
        return [Request('http://zhjw.scu.edu.cn/login',meta={'cookiejar':1},callback=self.parse)]

    def parse(self, response):     #parse回调函数
        # 响应Cookie
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print(Cookie1)
        print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        return [FormRequest.from_response(response,
                                          url='http://zhjw.scu.edu.cn/j_spring_security_check',   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          headers=self.header,
                                          formdata=self.logindata,
                                          callback=self.next,
                                          )]
    def next(self,response):
        a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback',meta={'cookiejar':True},callback=self.next2)
    def next2(self,response):
        # 请求Cookie
        Cookie2 = response.request.headers.getlist('Cookie')
        print(Cookie2)
        rs=json.loads(response.body)
        allmsg=rs['xkxx'][0]
        for key in allmsg:
            for sameclass in allmsg[key]['timeAndPlaceList']:
                classSchedule = classScheduleItem()
                classSchedule['userID'] = user.objects.get(userID=self.usermsg['userID'])
                classSchedule['attendClassTeacher'] = allmsg[key]['attendClassTeacher']
                classSchedule['courseName'] = allmsg[key]['courseName']
                classSchedule['classroomName'] = sameclass['campusName']+sameclass['teachingBuildingName']+sameclass['classroomName']
                classSchedule['weekDescription']= sameclass['weekDescription']
                classSchedule['classDay'] = sameclass['classDay']
                classSchedule['classSessions'] = sameclass['classSessions']
                classSchedule['continuingSession'] = sameclass['continuingSession']
                yield classSchedule






