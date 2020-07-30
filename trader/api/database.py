from django.conf import settings
from mongoengine import connect


def mongo_uri():
    if not settings.DEBUG:
        return (
            "mongodb://"
            + MONGO_DATABASE["USER"]
            + ":"
            + MONGO_DATABASE["PASSWORD"]
            + "@"
            + MONGO_DATABASE["HOST"]
            + ":"
            + MONGO_DATABASE["PORT"]
            + "/"
            + MONGO_DATABASE["DBNAME"]
        )
    else:
        return "mongodb://localhost:27017/smallcase"

def connect_mongo():
    connect(host=mongo_uri())
