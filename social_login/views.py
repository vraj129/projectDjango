from django.shortcuts import render, redirect
from django.conf import settings
# from django.contrib.auth.models import User


# Create your views here.
def index_page(request):
    data = {
        'project_name': settings.PROJECT_NAME,
    }
    return render(request, 'index.html', data)


def inactive_account(request):
    current_user = request.user
    if not current_user.is_active:
        return render(request, 'inactive_account.html')
    else:
        return redirect('/')
