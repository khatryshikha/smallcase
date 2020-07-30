from django.urls import path
from django.views.generic import RedirectView

from api.views import TradeView


urlpatterns = [path("trade/", TradeView.as_view(), name="trade")]
