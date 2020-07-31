import datetime

from django.http import JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views.generic import View

from api.models import Portfolio, Trades
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title="Portfolio Tracker APIs")


class TradeView(View):
    # Adding the trade details to DB
    def post(self, request):
        try:
            # Input data of the trade
            data_ticker = (str(request.POST.get("ticker_symbol", ""))).upper()
            data_buy_price = float(request.POST.get("buy_price", ""))
            data_shares_count = int(request.POST.get("shares_count", ""))
            data_trade_operation = (
                str(request.POST.get("trade_operation", ""))
            ).capitalize()

            # Creating a embedded document object for Portfolio object
            trade_obj = Trades(
                operation=data_trade_operation,
                ticker_symbol=data_ticker,
                shares_count=data_shares_count,
                buy_price=data_buy_price,
            )

            # Validation check
            if not trade_obj.is_valid():
                return JsonResponse(
                    {
                        "status": "fail",
                        "message": "Invalid input! Black fields and negative shares values are not allowed",
                    },
                    status=400,
                )

            # Checking the existance of the security for the given ticker symbol
            portfolio_obj_exist = Portfolio.objects(
                trades__match={"ticker_symbol": data_ticker}
            )

            if not len(portfolio_obj_exist):
                # If till yet no trade for given security, add the trade and updating portfolio
                portfolio_obj = Portfolio(
                    average_buy_price=data_buy_price,
                    total_shares_count=data_shares_count,
                    trades=[trade_obj],
                )
                portfolio_obj.save()

            else:
                # else update the existing security and add new trade to it
                portfolio_shares_count = int(
                    portfolio_obj_exist[0]["total_shares_count"]
                )
                portfolio_average_buy_price = float(
                    portfolio_obj_exist[0]["average_buy_price"]
                )
                portfolio_trades_list = portfolio_obj_exist[0]["trades"]

                # Check for trade operation
                if data_trade_operation == "Buy":
                    cumulative_shares = portfolio_shares_count + data_shares_count
                    cumulative_buy_price = (
                        portfolio_average_buy_price * portfolio_shares_count
                    ) + (data_buy_price * data_shares_count)
                    average_buy_price = cumulative_buy_price / cumulative_shares
                elif data_trade_operation == "Sell":
                    cumulative_shares = portfolio_shares_count - data_shares_count
                    average_buy_price = portfolio_average_buy_price

                portfolio_trades_list.append(trade_obj)

                # Updating the trade in DB
                portfolio_obj_exist.update(
                    set__total_shares_count=cumulative_shares,
                    set__average_buy_price=average_buy_price,
                    set__trades=portfolio_trades_list,
                )

            return JsonResponse(
                {"status": "success", "message": "Trade successfully done"}, status=200
            )

        except Exception as e:
            print(str(e))
            return JsonResponse(
                {"status": "fail", "message": "Trade failed due to server error"},
                status=500,
            )

    # Deleting the trade
    def delete(self, request):
        try:
            # Input data of the trade
            data = QueryDict(request.body)
            data_ticker = (str(data.get("ticker_symbol"))).upper()
            data_shares_count = int(data.get("shares_count"))
            data_buy_price = float(data.get("buy_price"))
            data_trade_operation = (str(data.get("trade_operation"))).capitalize()

            # Querying the document security for given trade ticker
            trade_obj = Portfolio.objects(
                trades__match={
                    "ticker_symbol": data_ticker,
                    "shares_count": data_shares_count ,
                    "buy_price": data_buy_price,
                }
            )

            if not len(trade_obj):
                return JsonResponse(
                    {"status": "fail", "message": "No such trade exist"}, status=404,
                )

            security_dict = trade_obj[0]["uid"]

            # deleting the trade from that security
            trade_obj.update_one(
                pull__trades__operation=data_trade_operation
            )

            portfolio_obj = Portfolio.objects(uid=security_dict)

            if not len(trade_obj):
                portfolio_obj.delete()
            else:
                changed_total_shares = int(
                    portfolio_obj[0]["total_shares_count"]
                ) - data_shares_count
                changed_average_buy_price = float(
                    portfolio_obj[0]["average_buy_price"]
                ) - float(data_buy_price * data_shares_count)

                portfolio_obj.update(
                    set__average_buy_price=changed_average_buy_price,
                    set__total_shares_count=changed_total_shares,
                )

            return JsonResponse(
                {"status": "success", "message": "Trade deletion Successfully"},
                status=200,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "fail",
                    "message": "Trade deletion failed due to server error",
                },
                status=500,
            )

    # Updating the existing trade with only changes in shares and buy_price
    def put(self, request):
        try:
            # Input data contains both old details and to update details
            data = QueryDict(request.body)
            data_ticker = (str(data.get("ticker_symbol"))).upper()
            data_shares_count = int(data.get("shares_count"))
            data_buy_price = float(data.get("buy_price"))
            data_trade_operation = (str(data.get("trade_operation"))).capitalize()

            # Querying the trade for given details
            trade_obj = Portfolio.objects(
                trades__match={
                    "ticker_symbol": data_ticker,
                    "shares_count": data_shares_count,
                    "buy_price": data_buy_price,
                    "operation": data_trade_operation,
                }
            )

            # Update only when trade exists
            if len(trade_obj):

                security_dict = trade_obj[0]["uid"]

                update_data_share_count = data.get(
                    "updated_shares_count", data_shares_count
                )
                update_buy_price = data.get(
                    "updated_buy_price", data_buy_price
                )

                trade_obj.update_one(
                    set__trades__S=Trades(
                        operation=data_trade_operation,
                        ticker_symbol=data_ticker,
                        shares_count=update_data_share_count,
                        buy_price=update_buy_price,
                        timestamp=datetime.datetime.now(),
                    )
                )
                portfolio_obj = Portfolio.objects(uid=security_dict)
                changed_total_shares = int(
                    portfolio_obj[0]["total_shares_count"]
                ) - data_shares_count + int(update_data_share_count)

                portfolio_obj.update(
                    set__total_shares_count=update_data_share_count,
                )
                return JsonResponse(
                    {"status": "success", "message": "Trade updated Successfully"},
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "status": "fail",
                        "message": f'No such trade exist for {data_ticker}',
                    },
                    status=404,
                )

        except Exception as e:
            return JsonResponse(
                {
                    "status": "fail",
                    "message": "Trade update failed due to server error",
                },
                status=500,
            )
