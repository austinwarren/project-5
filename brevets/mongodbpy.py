from pymongo import MongoClient
import os

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.mydb
collection = db.lists

def insert_brevet(brev_dist, start_time, items):
    """
    Inserts a new to-do list into the database "mydb", under the collection "lists".
    
    Inputs a distance(int) and items (list of dictionaries)
    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "brev_dist": brev_dist,
        "start_time":start_time,
        "items": items})
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)


def get_brevet():
    
    """
    Obtains the newest document in the "lists" collection in database "todo".
    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for i in lists:
        # We store all of our lists as documents with two fields:
        ## title: string # title of our to-do list
        ## items: list   # list of items:

        ### every item has two fields:
        #### desc: string   # description
        #### priority: int  # priority
        return i["brev_dist"], i["start_time"],i["items"]
