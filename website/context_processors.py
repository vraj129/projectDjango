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
                'verified_profile': extra_user_detail.verified_profile,
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


def device_data(request):
    # Mobile device detection Starts
    # Let's assume that the visitor uses an iPhone...
    request.user_agent.is_mobile  # returns True
    request.user_agent.is_tablet  # returns False
    request.user_agent.is_touch_capable  # returns True
    request.user_agent.is_pc  # returns False
    request.user_agent.is_bot  # returns False

    # Accessing user agent's browser attributes
    request.user_agent.browser  # returns Browser(
    # family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    request.user_agent.browser.family  # returns 'Mobile Safari'
    request.user_agent.browser.version  # returns (5, 1)
    request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    request.user_agent.os  # returns OperatingSystem(
    # family=u'iOS', version=(5, 1), version_string='5.1')
    request.user_agent.os.family  # returns 'iOS'
    request.user_agent.os.version  # returns (5, 1)
    request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    request.user_agent.device  # returns Device(family='iPhone')
    request.user_agent.device.family  # returns 'iPhone'
    # Mobile device detection Ends

    # return an empty dict if you want to return nothing
    return {}
