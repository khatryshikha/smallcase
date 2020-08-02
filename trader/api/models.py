# Create your models here.
import datetime
import uuid

from mongoengine import *


class Trades(EmbeddedDocument):
    operation = StringField(max_length=200, required=True)
    ticker_symbol = StringField(max_length=200, required=True)
    shares_count = IntField(min_value=0)
    buy_price = DecimalField(default=0)
    timestamp = DateTimeField(default=datetime.datetime.now)

    def is_valid(self):
        return (
            self.ticker_symbol != ""
            and self.buy_price != ""
            and (self.shares_count != "" and self.shares_count > 0)
        )


class Portfolio(Document):
    uid = UUIDField(default=uuid.uuid4, unique=True, editable=False)
    average_buy_price = DecimalField()
    total_shares_count = IntField(min_value=0)
    trades = EmbeddedDocumentListField(Trades)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {"indexes": ["uid"]}

