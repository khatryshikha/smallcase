# Create your models here.
from mongoengine import *
import datetime


class Trades(EmbeddedDocument):
    operations = StringField(max_length=200, required=True)
    shares = IntField(min_value=0)
    buy_price = DecimalField(default=0)
    timestamp = DateTimeField(default=datetime.datetime.now)


class Portfolio(Document):
    ticker_symbol = StringField(max_length=200, required=True)
    avg_buy_price = DecimalField()
    total_shares = IntField(min_value=0)
    trades = EmbeddedDocumentListField(Trades)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    meta = {"indexes": ["ticker_symbol"]}

    def is_valid(self):
        return (
            self.ticker_symbol != ""
            and self.avg_buy_price != ""
            and (self.total_shares != "" and self.total_shares > 0)
        )
