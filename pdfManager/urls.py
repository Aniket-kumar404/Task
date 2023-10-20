from django.urls import path,include
from . import views
from django.contrib import admin


urlpatterns = [
    path('home', views.home, name='home'),
    path('combineTwopdf', views.combineTwopdf, name='combineTwopdf'),
    path('removepdf', views.removepdf, name='removepdf'),
    path('extractall', views.extractall, name='extractall'),
    path('convert', views.convert, name='convert'),
    path('separate', views.separatePdf, name='separatePdf'),

 
]