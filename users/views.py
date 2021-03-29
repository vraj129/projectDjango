from django.shortcuts import redirect
from django.conf import settings
# import json
import urllib.request
import uuid
from extra_user_detail.models import Extra_User_Detail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from allauth.socialaccount.models import SocialAccount
from django_ip_geolocation.decorators import with_ip_geolocation


my_database = settings.CLIENT[settings.DATABASE_NAME]

# Create your views here.


# @login_required
# def full_profile(request):
#     # Getting data from collection -> `auth_user`
#     collection_name = "auth_user"
#     my_collection = my_database[collection_name]
#     auth_user_result = my_collection.find_one()

#     # Getting data from collection -> `socialaccount_socialaccount`
#     collection_name = "socialaccount_socialaccount"
#     my_collection = my_database[collection_name]
#     socialaccount_socialaccount_result = my_collection.find_one()

#     # Extracting Extra Data
#     my_query = {"id": 1}  # id == 1
#     my_fields = {"_id": 0, "extra_data": 1}  # exclude `_id`, include `extra_data`
#     documents = my_collection.find(my_query, my_fields)

#     document = documents[0]
#     for key, value in document.items():
#         # Converting extra_data from String to DICT
#         res = json.loads(value)

#     print(res["picture"])
#     return render(request, 'user_data.html', {
#         'auth_user_data': auth_user_result,
#         'socialaccount_socialaccount_data': socialaccount_socialaccount_result,
#         'socialaccount_socialaccount_extra_data': res,
#     })


@with_ip_geolocation
@login_required
def profile_picture(request):
    # Getting location based on IP
    location = request.geolocation
    print(location, " *Location is approximate based on the login's IP address.")

    # Getting Current Logged in User
    current_user = request.user

    username = User.objects.get(username=current_user.username)

    # ===== Check if entry already exists | Start =====

    # If `get` method finds no entry or finds multiple entries,
    # it raises an exception
    try:
        extra_user_detail = Extra_User_Detail.objects.get(user=username)
    except Extra_User_Detail.DoesNotExist:
        extra_user_detail = None

    print("==================================")
    print(extra_user_detail)

    # ===== Check if entry already exists | Ends =====

    # If user pic DoesNotExists
    if extra_user_detail is None:
        print("----------------------------------")

        # Getting `id` fo Currently Logged in User
        print("New User logged in: User id: ", current_user.id)

        # Python and Mongo Code Starts =================================
        # # Setting Collection to be used
        # collection_name = "socialaccount_socialaccount"
        # my_collection = my_database[collection_name]

        # # Extracting Field named `extra_data`
        # # from collection named  `socialaccount_socialaccount` of Current User
        # my_query = {"user_id": current_user.id}  # id == 1
        # my_fields = {"_id": 0, "extra_data": 1}  # exclude `_id`, include `extra_data`
        # documents = my_collection.find(my_query, my_fields)

        # document = documents[0]  # Because the result `documents` is iterable

        # # Getting Value of Field named `extra_data`
        # extra_data = document["extra_data"]
        # Python and Mongo Code Ends =================================

        # Python and Django Code Starts =================================
        try:
            socialaccount_socialaccount_data = SocialAccount.objects.get(
                user=current_user.id)
            extra_data = socialaccount_socialaccount_data.extra_data
        except SocialAccount.DoesNotExist:
            print("Not Exists, Jai Swaminarayan")
        # Python and Django Code Ends =================================

        # Converting `extra_data` from String to Dict
        # res = json.loads(extra_data)

        # Getting value of field `picture`
        profile_pic_url = extra_data["picture"]

        # Getting Value of field `locale`
        locale = extra_data["locale"]

        # Drawback of uuid1() :
        # This way includes the used of MAC address of computer, and hence can
        # compromise the privacy, even though it provides uniquenes.

        # Using uuid4()
        # This function guarantees the random no. and doesn’t compromise with privacy.

        # Generating random string for image name
        image_name = uuid.uuid4()

        # Path to save the image
        path_to_save_image = "media/profile_pictures/" + image_name.hex + ".jpg"

        # Saving Url Image in the path
        urllib.request.urlretrieve(profile_pic_url, path_to_save_image)

        # We cannot use `current_user.username` directly
        # in line: Extra_User_Detail(user=username, ...)

        # It needs to be an instance of the User model
        username = User.objects.get(username=current_user.username)

        # Saving User Details
        new_user_profile = Extra_User_Detail(user=username,
                                             image_url=path_to_save_image,
                                             locale=locale)
        new_user_profile.save()

    if 'url_to_go' in request.session:
        return redirect(request.session.get('url_to_go'))
    else:
        return redirect('/')


def signout(request):
    auth.logout(request)
    return redirect('/')
