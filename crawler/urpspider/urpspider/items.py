# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from warehouse.models import urpScrapy,user


class classScheduleItem(DjangoItem):
    django_model = urpScrapy

class userItem(DjangoItem):
    django_model=user
