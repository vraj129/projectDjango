from django.shortcuts import render
from django.conf import settings


# Create your views here.
def listDatabases(request):
    print(settings.CLIENT)
    data = {}

    # # List Databases
    # for name in client.list_database_names():
    #     print(name)

    # # List Collections
    # for collection_name in client.get_database('tuc').list_collection_names():
    #     print(collection_name)

    # my_database = client["tuc"]
    # my_collection = my_database["auth_user"]
    # count = my_collection.count_documents({})

    # data["auth_user"] = count

    # ===============================================

    dbname = "tuc"
    my_database = settings.CLIENT[dbname]
    for collection_name in settings.CLIENT.get_database(dbname).list_collection_names():
        my_collection = my_database[collection_name]

        # Couning Document in each Collection
        count = my_collection.count_documents({})

        # Appending To Dictionary
        data[collection_name] = count
    # ================================================
    return render(request, 'listDatabases.html', {'data': data})


def base(request):
    data = {
        'project_name': settings.PROJECT_NAME,
    }
    return render(request, 'base.html', data)
