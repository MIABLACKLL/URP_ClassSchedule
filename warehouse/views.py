from django.shortcuts import render,render_to_response
from .models import user
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor,defer
from scrapy.utils.log import configure_logging
import requests
import os
from crochet import setup
setup()

def login(request):
    formData = {'j_username': '0', 'j_password': '0', 'j_captcha1': 'error'}
    ip="localhost"
    port=6800
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        formData['j_username']=username
        formData['j_password']=password
        if user.objects.filter(userID=formData['j_username'],userPassword=formData['j_password']).exists():#之前已登录过，直接从数据库中验证
            return render_to_response('success.html',{'username':username})
        else:
            session = requests.session()
            response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
            check_login = session.get(url='http://zhjw.scu.edu.cn/index.jsp', allow_redirects=False)
            code = check_login.status_code
            if code < 300:
                os.chdir(r'E:\PythonProgram\program\urp_scrapy\crawler\urpspider\urpspider')
                crawler_settings = get_project_settings()
                crawler = CrawlerRunner(crawler_settings)
                configure_logging()
                crawler.crawl('urplogin', logindata=formData)
                return render_to_response('success.html', {'username': username})
            else:
                return render(request, 'login.html')#密码错误

#def index(request):








