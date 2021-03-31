from django.urls import (
    path,
    # re_path
)
# from django.conf.urls import url
from . import views


urlpatterns = [
    path('new/', views.new, name='New Page'),
    path('edit/<slug:slug>/', views.edit, name='Edit Page'),
    path('discard-article/', views.discardArticle, name='Discard Article'),
    path('publish/', views.publish, name='Publish Page'),

    path("save_article/$", views.save_article, name='save_article'),
    path("get_categories/$", views.get_categories, name='get_categories'),
    path("confirm_publish/$", views.confirm_publish, name='confirm_publish'),
    path("report_article/$", views.report_article, name='report_article'),

    path('<str:url_title>/', views.dynamic_article, name='Default Page'),
    path('<str:url_title>/pdf/', views.dynamic_article_as_pdf, name='PDF Page'),
]
