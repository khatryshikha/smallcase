# Create your models here.
from mongoengine import *
import datetime


class Testing(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
