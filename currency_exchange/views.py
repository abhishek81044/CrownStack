from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from . import xchange_calculator
from . import models as Model 
from rest_framework.views import APIView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import json

class Views(viewsets.ViewSet):

    @action(detail=False, methods=['POST'])
    def get_currency_exchange(request):
        try:
            sel_cur = request.POST.get('drop')

            get_abbrev = Model.currency_details.objects.filter(currency_name=sel_cur).last()

            sel_cur_abbrev = get_abbrev.currency_abbrev

            process = xchange_calculator.GetXchange()
            gx = process.process(sel_cur_abbrev)
            res = json.loads(gx.text)

            currency_model = Model.currency_details.objects.all()
            currency_list = []
            xchange_list = {}
            for item in currency_model:
                currency_list.append(item.currency_name)
                if sel_cur_abbrev == item.currency_abbrev:
                    continue
                else:
                    xchange_list[item.currency_name] = res["rates"][item.currency_abbrev]

        
            return render(request, 'index.html', {'currency_list':currency_list,'res':xchange_list,'sel_cur':sel_cur})
        except Exception as ex:
            return HttpResponse(ex, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_currency_list(request):
        try:
            # get currency list from database
            currency_model = Model.currency_details.objects.all()

            currency_list = []
            if currency_model:
                for item in currency_model:
                    currency_list.append(item.currency_name)
            
            return render(request, 'index.html', {'currency_list':currency_list})
        except Exception as ex:
            return HttpResponse(ex, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def add_currency_list(request):
        try:
            # get currency list from database
            currency_list = ["Indian Rupee (INR)","Australian Dollar (AUD)","Canadian Dollar (CAD)","Japanese Yen (JPY)"]
            currency_abbrev = ["INR","AUD","CAD","JPY"]
            for i in range(len(currency_list)):
                currency_model = Model.currency_details()
                currency_model.currency_name = currency_list[i]
                currency_model.currency_abbrev = currency_abbrev[i]
                currency_model.save()

            return HttpResponse("Added Successfully", status = status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponse(ex, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
