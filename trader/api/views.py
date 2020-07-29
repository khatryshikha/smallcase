from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View
from api.models import Testing

class TradeView(View):
    def get(self, request):
        testing_docs = Testing.objects()
        print(testing_docs)
        print("inside get")
        return HttpResponse("hello get")

    def post(self, request):
        try:
            page = Testing(title='Using MongoEngine')
            page.save()
            return HttpResponse("hello post")
        except Exception as exc:
            print(str(exc))
            return "uh oh"
