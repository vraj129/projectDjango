import os
from tuc.settings import BASE_DIR


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # None is written to handle Errors
        # If In case Unable to get the client's IP address
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def delete_realted_data(obj):
    print(obj.file_location)
    article_file_path = os.path.join(BASE_DIR) + '/' + obj.file_location
    if os.path.exists(article_file_path):
        os.remove(article_file_path)
        print("Deleted File")
