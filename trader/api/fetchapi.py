from django.http import JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views.generic import View

from api.models import Portfolio, Trades


class FetchView(View):

    # Fetching the portfolio for all securities and trades corresponding
    def get(self, request):
        try:
            portfolio_list = []

            for protfolio in Portfolio.objects:
                dict_obj = dict(protfolio.to_mongo())
                dict_obj["_id"] = str(dict_obj["_id"])
                portfolio_list.append(dict_obj)

            return JsonResponse(
                {"portfolio": portfolio_list, "status": "success"}, status=200
            )
        except Exception as e:
            return Http
            return JsonResponse(
                {"status": "fail", "message": "Failed to fetch portfolio"}, status=500
            )


class FetchHoldingView(View):
    # Fetching the holdings and final quantity of shares
    def get(self, request):
        try:
            total_holdings = 0
            portfolio_obj = Portfolio.objects
            total_holdings = sum(
                float(portfolio["total_shares_count"] * portfolio["average_buy_price"])
                for portfolio in portfolio_obj
            )
            return JsonResponse(
                {
                    "total securities": len(portfolio_obj),
                    "holdings": total_holdings,
                    "status": "success",
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "fail", "message": "Failed to fetch holdings"}, status=500
            )


class FetchReturnsView(View):

    # Fetching the returns with assumption of current price is Rs. 100 for any security
    def get(self, request):
        try:
            total_holdings = 0
            portfolio_obj = Portfolio.objects
            total_holdings = sum(
                float(portfolio["total_shares_count"] * portfolio["average_buy_price"])
                for portfolio in portfolio_obj
            )
            returns = (100 * portfolio_obj[0]["total_shares_count"]) - total_holdings

            return JsonResponse({"returns": returns, "status": "success"}, status=200)
        except Exception as e:
            return JsonResponse(
                {"status": "fail", "message": "Failed to fetch returns"}, status=500
            )
