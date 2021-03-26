"""tuc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from social_login.views import inactive_account
# from tuc.decorators import staff_required


# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#adminsite-objects


# admin.site.login = staff_required(admin.site.login)
# https://stackoverflow.com/questions/66673368/how-to-restrict-non-staff-users-from-accessing-django-admin/

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN_REDIRECT_URL is defined in settings.py
    path('social_login/', include('social_login.urls')),
    path('', include('website.urls')),
    path('user/', include('users.urls')),
    path('article/', include('article.urls')),

    path('accounts/inactive/', inactive_account, name='Inactive acc'),
    path('accounts/', include('allauth.urls')),

    path('curd/', include('curd.urls')),
]

# Media Visibilty in Website
urlpatterns = urlpatterns + static(settings.MEDIA_URL,
                                   document_root=settings.MEDIA_ROOT)
