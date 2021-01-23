from django.conf import settings
from extra_user_detail.models import Extra_User_Detail
from django.contrib.auth.models import User


def basic_data(request):
    if request.user.is_authenticated:
        current_user = request.user
        username = User.objects.get(username=current_user.username)
        try:
            extra_user_detail = Extra_User_Detail.objects.get(user=username)
        except Extra_User_Detail.DoesNotExist:
            extra_user_detail = None

        if extra_user_detail is not None:
            data = {
                'project_name': settings.PROJECT_NAME,
                'profile_picture': "/" + extra_user_detail.image_url,
                'locale': extra_user_detail.locale,
            }
        else:
            data = {
                'project_name': settings.PROJECT_NAME,
            }

    # if user not authenticated
    else:
        data = {
            'project_name': settings.PROJECT_NAME,
        }
    return data
