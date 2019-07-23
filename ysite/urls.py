from django.contrib import admin
from django.urls import path
from rstie.views import read, write, maiin, creating, login_page, logout_page, register, otziv, otziv_read

urlpatterns = [
    path('readeedback/', otziv_read),
    path('feedback/', otziv),
    path('register/', register),
    path('logout/', logout_page),
    path('login/', login_page),
    path('admin/', admin.site.urls),
    path('', maiin),
    path('read/', read),
    path('write/', write),
    path('create/', creating),
]
