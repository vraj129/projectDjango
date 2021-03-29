from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib import admin
from django.conf import settings


admin.site.site_header = settings.PROJECT_NAME
admin.site.index_title = 'Apps'
admin.site.site_title = settings.PROJECT_NAME

urlpatterns = [
    path('', views.home, name='Home Page'),
    path('new/', views.new, name='New Page'),
    # path('new/', views.new2, name='New Page'),
    # path('new/<slug:slug>/', views.new, name='New Page'),
    # path('edit/<slug:slug>/', views.edit, name='Edit Page'),

    # Editing Article
    # path(r'edit/(?P<string>[\w\-]+)/$', views.edit, name='Edit Page'),
    # url(r'^edit/(?P<slug>[\w-]+)/$', views.edit, name='blog_detail'),
    # url(r'^edit/([\w]+)$', views.edit), # Correct /edit/1
    # url(r'^edit/([\w\-]+)$', views.edit),
    # url(r'^edit/$', views.edit),
    # re_path(r'^edit/(?P<url_title>[0-9]{4})/$', views.edit),
    # path('edit/<slug:slug>/', views.edit, name='Edit Page'),

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
    path("report_article/$", views.report_article, name='report_article'),
]
