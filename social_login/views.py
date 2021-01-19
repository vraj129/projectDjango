from django.shortcuts import render
from django.conf import settings


# Create your views here.
def index_page(request):
    data = {
        'project_name': settings.PROJECT_NAME,
    }
    return render(request, 'index.html', data)
