from django.urls import path
from . import views

urlpatterns = [
    # path('profile/', views.full_profile, name="Getting Profile Data"),
    path('profile/picture/', views.profile_picture, name="Getting Profile Picture"),
    path('signout/', views.signout, name="Signout"),
]
