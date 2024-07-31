from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://aabselyam:N3ME97j33WUwAuUt@cluster0.asrrhco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["neoversity"]
collection = db["neoversity"]


def create_cat(name, age, features):
    cat = {"name": name, "age": age, "features": features}
    collection.insert_one(cat)
    print(f"Cat {name} added to the collection.")


def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)


def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat found with name {name}.")


def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Cat {name}'s age updated to {new_age}.")
    else:
        print(f"No cat found with name {name}.")


def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.modified_count > 0:
        print(f"Feature '{feature}' added to cat {name}.")
    else:
        print(f"No cat found with name {name}.")


def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Cat {name} deleted from the collection.")
    else:
        print(f"No cat found with name {name}.")


def delete_all_cats():
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} cats from the collection.")


if __name__ == "__main__":
    create_cat("Tom", 3, ["cute", "playful"])
    create_cat("Jerry", 2, ["naughty", "smart"])

    read_all_cats()

    read_cat_by_name("Tom")

    update_cat_age("Tom", 4)

    add_feature_to_cat("Tom", "sleepy")

    delete_cat_by_name("Jerry")

    delete_all_cats()

    read_all_cats()

    client.close()
