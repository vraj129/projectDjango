from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='Home Page'),
    path('new/', views.new, name='New Page'),
    # path('explore/', views.explore, name='Explore'),
    path('logout/', views.logout, name='Logout Page'),
    path('base/', views.base, name='Base'),
    path('tnc/', views.terms_and_conditions, name='TnC'),
    path('contact/', views.contact, name='Contact'),
]
