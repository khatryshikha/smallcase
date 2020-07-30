from django.http import Http404, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views.generic import View

from api.models import Portfolio


class FetchView(View):

    """
    
        Fetching all Portfolios, total asset holding and 
        its return with consideration of current price = Rs 100 for each security.
    """

    def get(self, request):
        try:
            total_returns = 0
            total_holding = 0
            total_share_count = 0
            Portfolios = []
            for trade in Portfolio.objects:
                total_share_count += trade["shares"]
                total_holding += trade["shares"] * trade["avg_buy_price"]
                temp = dict(trade.to_mongo())
                temp["_id"] = str(temp["_id"])
                Portfolios.append(temp)

            total_returns = 100 * total_share_count - total_holding

            context = {
                "Total Returns": total_returns,
                "Total Holdings": total_holding,
                "Portfolios": Portfolios,
            }
            return JsonResponse(context)
        except Exception as e:
            return JsonResponse(
                {
                    "code": "1",
                    "status": "failed",
                    "Message": "Failed to fetch Portfolio details",
                }
            )
