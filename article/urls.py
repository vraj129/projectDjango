from django.urls import path
from . import views


urlpatterns = [
    path('<str:url_title>/', views.dynamic_article, name='Default Page'),
    path('<str:url_title>/pdf/', views.dynamic_article_as_pdf, name='PDF Page'),
]
