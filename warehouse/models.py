from django.db import models


class urpScrapy(models.Model):
    userID=models.ForeignKey(to='user',to_field='userID',on_delete=models.CASCADE,default='')
    courseName =models.CharField(max_length=255,default='')   # 课程名字
    attendClassTeacher =models.CharField(max_length=255,default='')  # 该课教师名字
    classroomName =models.CharField(max_length=255,default='')   # 校区、教学楼及教室
    weekDescription =models.CharField(max_length=255,default='')  # 上课周期
    classDay =models.CharField(max_length=255,default='')   # 星期
    classSessions =models.CharField(max_length=255,default='')  # 开始节数
    continuingSession =models.CharField(max_length=255,default='')   # 持续节数

    class Meta:
        app_label = 'warehouse'
        db_table = 'classschedule'

class user(models.Model):

    userID=models.CharField(max_length=255,default='',unique=True)
    userPassword = models.CharField(max_length=255, default='')
    userName=models.CharField(max_length=255,default='')
    class Meta:
        app_label = 'warehouse'
        db_table = 'user'