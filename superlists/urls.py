from django.contrib import admin
from django.urls import path, re_path, include

from lists import urls as lists_urls
from accounts import urls as accounts_urls
from lists import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^lists/', include(lists_urls)),
    re_path(r'^accounts/', include(accounts_urls)),
]
