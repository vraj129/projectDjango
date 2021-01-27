from django.urls import path
from . import views


urlpatterns = [
    path('<str:url_title>', views.dynamic_article, name='Default Page'),
    path('demo/demo/', views.demo, name='Default Page'),
]
