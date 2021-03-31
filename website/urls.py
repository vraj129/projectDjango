from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings


admin.site.site_header = settings.PROJECT_NAME
admin.site.index_title = 'Apps'
admin.site.site_title = settings.PROJECT_NAME

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('logout/', views.logout, name='Logout Page'),
    path('base/', views.base, name='Base'),
    path('tnc/', views.terms_and_conditions, name='TnC'),
    path('contact/', views.contact, name='Contact'),
]
