from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import urpScrapy, user
import requests
from scrapy_djangoitem import DjangoItem
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse, JsonResponse
from django.core import serializers

formData = {'j_username': '0', 'j_password': '0', 'j_captcha1': 'error'}
def login(request):
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
            return HttpResponseRedirect( '/success')
        else:
            session = requests.session()
            response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
            check_login = session.get(url='http://zhjw.scu.edu.cn/index.jsp', allow_redirects=False)
            code = check_login.status_code
            if code < 300:
                run_crawl(formData)
                return HttpResponseRedirect('/success')
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


def index(request):
    if request.method == 'GET':
        msg = urpScrapy.objects.filter(userID=formData['j_username'])
        json_data = serializers.serialize('json', msg)
        json_data = json.loads(json_data)
        msgdict = {}
        i = 0
        for eachmsg in json_data:
            string = str(i)
            msgdict[string] = eachmsg['fields']
            i += 1
        msgstr = str(msgdict)
        msgstr = msgstr.replace("'", "\"")
        json_data = json.loads(msgstr)
        with open("msg.json", "w") as f:
            json.dump(json_data, f, ensure_ascii=False)
        return render("success.html",json_data)



