'''

def setup_django_env():
    import os, django,sys
    sys.path.extend(['E:\\PythonProgram\\program\\urp_scrapy'])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urp_scrapy.settings")
    django.setup()

def check_db_connection():
    from django.db import connection

    if connection.connection:
        #NOTE: (zacky, 2016.MAR.21st) IF CONNECTION IS CLOSED BY BACKEND, CLOSE IT AT DJANGO, WHICH WILL BE SETUP AFTERWARDS.
        if not connection.is_usable():
            connection.close()
'''