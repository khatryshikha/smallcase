from django.urls import path
from django.views.generic import RedirectView

from api.views import TradeView
from api.fetchingAPIs import FetchView


urlpatterns = [
    path("trade/", TradeView.as_view(), name="trade"),
    path("fetch/", FetchView.as_view(), name="fetch"),
]
