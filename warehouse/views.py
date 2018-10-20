from django.shortcuts import render

# Create your views here.
import requests

def get_login(request):
    formData = {'j_username': '0', 'j_password': '0', 'j_captcha1': 'error'}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        formData = {'j_username': username, 'j_password': password, 'j_captcha1': 'error'}
    return formData



def check_login(request):
        formData=get_login()
        session = requests.session()
        response = session.post(url='http://zhjw.scu.edu.cn/j_spring_security_check', data=formData)
        check_login = session.get(url='http://zhjw.scu.edu.cn/index.jsp', allow_redirects=False)
        code = check_login.status_code
        if code < 300:
            print("OK")
        else:
            return render(request, 'index.html')#登录失败
