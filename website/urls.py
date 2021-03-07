from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings


admin.site.site_header = settings.PROJECT_NAME
admin.site.index_title = 'Apps'
admin.site.site_title = settings.PROJECT_NAME

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('new/', views.new, name='New Page'),
    path('discard-article/', views.discardArticle, name='Discard Article'),
    path('publish/', views.publish, name='Publish Page'),
    # path('explore/', views.explore, name='Explore'),
    path('logout/', views.logout, name='Logout Page'),
    path('base/', views.base, name='Base'),
    path('tnc/', views.terms_and_conditions, name='TnC'),
    path('contact/', views.contact, name='Contact'),

    # Recieves Responses so that we can send back content
    # without refreshing page
    path("get_response/$", views.answer_me, name='get_response'),
    path("get_categories/$", views.answer_categories, name='get_categories'),
    path("confirm_publish/$", views.confirm_publish, name='confirm_publish'),
]
