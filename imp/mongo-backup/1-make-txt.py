import pymongo  # pip install pymongo
import sys
from pymongo.errors import ServerSelectionTimeoutError


def get_database_names():
    # If no Argument is passed all Databases backup is taken
    database_to_backup = []
    if(len(sys.argv) == 1):
        print("Backing Up All Databases...")

    else:
        for i, arg in enumerate(sys.argv):
            # Ignoring First Argument as it is name of Program
            if i == 0:
                continue
            database_to_backup.append(arg)

        print("Backing up these Databases...")
        print(database_to_backup)
    return database_to_backup


if __name__ == "__main__":
    database_to_backup = get_database_names()

    print("Connecting MongoClient...")
    # Connection String
    client = pymongo.MongoClient(
        "mongodb+srv://ajinzrathod:ajinz812@theunitedcodes.eump1.mongodb.net/"
        "tuc?retryWrites=true&w=majority")
    print("Done")

    if len(database_to_backup) < 1:
        for database_name in client.list_database_names():
            database_to_backup.append(database_name)

    collection_count = 0

    # Iterating Through each Database
    # for database_name in client.list_database_names():
    f = open("collections.txt", "w")
    for database_name in database_to_backup:
        print("\nAdding: " + database_name + "...")
        if database_name not in client.list_database_names():
            print("\"" + database_name + "\"" + " not found")
            continue

        # write to file
        f.write("-" + database_name + "\n")

        database = client[database_name]

        # Getting Collection Names
        collection = database.list_collection_names(
            include_system_collections=False)

        # Counting Collections
        collection_count += len(collection)

        # Iterating Through each collection
        if len(collection):
            for collect in collection:
                print("-", collect)
                # write to file
                f.write(collect + "\n")
        else:
            print("No Collections.")
        print("\"" + database_name + "\"" + " added to file")

    f.close()
    print("\nTotal " + str(collection_count) +
          " Collections found in " + str(len(database_to_backup)) +
          " Databases")
    print("Done.")
