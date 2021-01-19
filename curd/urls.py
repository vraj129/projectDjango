from django.urls import path
from . import views

urlpatterns = [
    path('documentcount/', views.listDatabases, name='List of Databases'),
    path('base/', views.base, name='Base'),
]
