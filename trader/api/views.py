import datetime

from django.http import Http404, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views.generic import View

from api.models import Portfolio


class TradeView(View):

    # Adding the trade details to DB
    def post(self, request):
        try:
            # Data of the trade
            ticker = str(request.POST.get("ticker_symbol", ""))
            buy_price = float(request.POST.get("avg_buy_price", ""))
            no_shares = int(request.POST.get("shares", ""))
            trade = f"Bought {no_shares} shares of {ticker} at {buy_price}"

            # Checking protofolio if the entry for same security exist.
            is_Portfolio_exist = Portfolio.objects(ticker_symbol=ticker)

            if not len(is_Portfolio_exist):
                # Adding the trade into the DB
                portfolio = Portfolio(
                    ticker_symbol=ticker,
                    avg_buy_price=buy_price,
                    shares=no_shares,
                    trades=[trade],
                )

                # Validation for NULL value or shares count less than 0
                if portfolio.is_valid():
                    portfolio.save()

                return JsonResponse(
                    {
                        "code": "0",
                        "status": "success",
                        "Message": "Successfully added the shares",
                    }
                )
            else:
                self.update(
                    ticker_symbol=ticker,
                    avg_buy_price=buy_price,
                    shares=no_shares,
                    is_add=True,
                )
                return JsonResponse(
                    {
                        "code": "0",
                        "status": "success",
                        "Message": "Security already exist, updated successfully!",
                    }
                )

        except Exception as exc:
            print(str(exc))
            return JsonResponse(
                {"code": "1", "status": "failed", "Message": "Failed to add the shares"}
            )

    def put(self, request):
        try:
            # Updated form details
            data = QueryDict(request.body)

            self.update(
                ticker_symbol=str(data.get("ticker_symbol")),
                avg_buy_price=float(data.get("avg_buy_price")),
                shares=int(data.get("shares")),
                is_add=False,
            )

            return JsonResponse(
                {
                    "code": "0",
                    "status": "success",
                    "Message": "Successfully updated the share",
                }
            )
        except Exception as e:
            print(str(e))
            return JsonResponse(
                {
                    "code": "1",
                    "status": "failed",
                    "Message": "Failed to update the share",
                }
            )

    # Delete the document for given ticker symbol
    def delete(slef, request):
        try:
            data = QueryDict(request.body)
            Portfolio.objects(ticker_symbol=str(data.get("ticker_symbol"))).delete()

            return JsonResponse(
                {
                    "code": "0",
                    "status": "success",
                    "Message": "Successfully deleted the share",
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "code": "1",
                    "status": "failed",
                    "Message": "Failed to delete the share",
                }
            )

    def update(self, **kwargs):

        # Input data
        data_shares = int(kwargs["shares"])
        data_avg_buy_price = float(kwargs["avg_buy_price"])
        data_ticker = str(kwargs["ticker_symbol"])
        data_is_add = kwargs["is_add"]

        # Retrieving existing data from DB
        Portfolio = Portfolio.objects.get(ticker_symbol=data_ticker)

        Portfolio_shares = int(Portfolio["shares"])
        Portfolio_avg_buy_price = float(Portfolio["avg_buy_price"])
        Portfolio_trade = Portfolio["trades"]

        # if update is via add functionality
        if data_is_add:
            shares = Portfolio_shares + data_shares
            buy_price = (Portfolio_avg_buy_price * Portfolio_shares) + (
                data_avg_buy_price * data_shares
            )
            avg_buy_price = buy_price / shares
            trade = (
                f"Bought {data_shares} shares of {data_ticker} at {data_avg_buy_price}"
            )
        else:
            # else update to the existing values
            shares = data_shares

            # if shares are sold
            if Portfolio_shares > data_shares:
                trade = f"Sold {Portfolio_shares - data_shares} shares of {data_ticker} at {data_avg_buy_price}"
                avg_buy_price = Portfolio_avg_buy_price
            else:
                # else bought the new shares
                buy_price = (Portfolio_avg_buy_price * Portfolio_shares) + (
                    data_avg_buy_price * (data_shares - Portfolio_shares)
                )
                avg_buy_price = buy_price / shares
                trade = f"Bought {data_shares - Portfolio_shares} shares of {data_ticker} at {data_avg_buy_price}"

        Portfolio_trade.append(trade)

        # Updating the document in DB
        Portfolio.update(
            set__shares=data_shares,
            set__avg_buy_price=avg_buy_price,
            set__trades=Portfolio_trade,
            set__timestamp=datetime.datetime.now(),
        )

        # Validating the entries
        if Portfolio.is_valid():
            return
        else:
            raise Exception("Invalid Input")
