from django.shortcuts import render
from .models import user
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import requests
import os
def login(request):
    formData = {'j_username': '0', 'j_password': '0', 'j_captcha1': 'error'}
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        formData['j_username']=username
        formData['j_password']=password
        if user.objects.filter(userID=formData['j_username'],userPassword=formData['j_password']).exists():#之前已登录过，直接从数据库中验证
            return render(request, 'index.html')
        else:
            session = requests.session()
            response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
            check_login = session.get(url='http://zhjw.scu.edu.cn/index.jsp', allow_redirects=False)
            code = check_login.status_code
            if code < 300:
                os.chdir(r'E:\PythonProgram\program\urp_scrapy\crawler\urpspider\urpspider')
                process = CrawlerProcess(get_project_settings())
                process.crawl('urplogin', logindata=formData)
                process.start()
                return render(request, 'index.html')
            else:
                return render(request, 'login.html')#密码错误

#def index(request):







