from django.shortcuts import render
from django.shortcuts import render
from ast import Try

from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http.request import HttpRequest
from .models import Order

def indexView(request: HttpRequest):

    # if request.session.get('samlUserdata'):
    #     samlUserdata = request.session.get('samlUserdata')
    # else:
    #     samlUserdata = None
    # print('samlUserdata:', samlUserdata)

    if request.method == "POST":
        searched = request.POST.get('searched', False)
        # searched = request.POST['searched']
        orders = Order.objects.filter(customer__contains=searched)
        return render(request, 'indexView.html', {'orders': orders, 'searched': searched}) # , 'samlUserdata': samlUserdata})
    else:
        return render(request, 'indexView.html', {'orders': None, 'searched': None}) #, 'samlUserdata': samlUserdata})

    # the third argument can be sent from view to template

def beforeLogin(request):
    return render(request, 'beforeLogin.html')


def order_detail(request, orderId):
    order = Order.objects.get(orderId=orderId)
    return render(request, 'order_detail.html', {'order': order})
