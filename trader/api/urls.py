from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url
from api.views import TradeView
from api.fetchapi import FetchView, FetchHoldingView, FetchReturnsView
from django.views.generic import TemplateView


urlpatterns = [
    path("",TemplateView.as_view(template_name="trade-form.html")),
    path("trade", TradeView.as_view(), name="trade"),
    path("fetch", FetchView.as_view(), name="fetch_portfolio"),
    path("fetch/holdings", FetchHoldingView.as_view(), name="fetch_holdings"),
    path("fetch/returns", FetchReturnsView.as_view(), name="fetch_returns"),
]
