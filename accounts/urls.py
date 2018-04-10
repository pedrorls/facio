from django.contrib.auth.views import logout
from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^send_login_email$', send_login_email, name='send_login_email'),
    re_path(r'^login$', login, name='login'),
    re_path(r'^logout$', logout, {'next_page': '/'}, name='logout',)
]
