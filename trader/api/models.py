# Create your models here.
from mongoengine import *
import datetime

class Trades(EmbeddedDocumentListField):
    operations = StringField(max_length=200, required=True)


class Portfolio(Document):
    ticker_symbol = StringField(max_length=200, required=True)
    avg_buy_price = DecimalField()
    shares = IntField(min_value=0)
    trades = EmbeddedDocumentListField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DataTimeFiled(Trades, default=Trades)
    meta = {"indexes": ["ticker_symbol"]}

    def is_valid(self):
        return (
            self.ticker_symbol != ""
            and self.avg_buy_price != ""
            and (self.shares != "" and self.shares > 0)
        )
