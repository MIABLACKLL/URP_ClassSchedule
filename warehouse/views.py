from django.shortcuts import render,render_to_response
from .models import urpScrapy, user
import requests
from scrapy_djangoitem import DjangoItem
import json
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
                run_crawl(formData)
                return render_to_response('success.html', {'username': username})
            else:
                return render(request, 'login.html')#密码错误

def run_crawl(formData):
    class classScheduleItem(DjangoItem):
        django_model = urpScrapy
    class userItem(DjangoItem):
        django_model = user
    session = requests.session()
    response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
    usermsg = userItem()
    usermsg['userID'] = formData['j_username']
    usermsg['userName'] = ""
    usermsg['userPassword'] = formData['j_password']
    usermsg.save()
    classscheduleURL = 'http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback'
    msg = session.get(url=classscheduleURL)
    rs = json.loads(msg.text)
    allmsg = rs['xkxx'][0]
    for key in allmsg:
        for sameclass in allmsg[key]['timeAndPlaceList']:
            classSchedule = classScheduleItem()
            classSchedule['userID'] = user.objects.get(userID=formData['j_username'])
            classSchedule['attendClassTeacher'] = allmsg[key]['attendClassTeacher']
            classSchedule['courseName'] = allmsg[key]['courseName']
            classSchedule['classroomName'] = sameclass['campusName'] + sameclass['teachingBuildingName'] + sameclass[
                'classroomName']
            classSchedule['weekDescription'] = sameclass['weekDescription']
            classSchedule['classDay'] = sameclass['classDay']
            classSchedule['classSessions'] = sameclass['classSessions']
            classSchedule['continuingSession'] = sameclass['continuingSession']
            classSchedule.save()









