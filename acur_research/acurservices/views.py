from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from acur_research.serializers import CheckHeadSerializer, CheckPositionSerializer, CheckPhoneNumberSerializer,PollResultSerializer
from acur_research.serializers import EvoUserSerializer
from acur_research.models import CheckHead, CheckPosition,WebhookTransaction, PollResult, EvoUser
from rest_framework import mixins
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from acur_research.analytic import poll_is_needed
from rest_framework.decorators import action
import logging
from twilio.rest import Client
from jsonschema import validate
import jsonschema

import copy, json, datetime
from rest_framework import permissions
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


#K0ymrcxHKM


from acur_research.acurservices.business_logic import run_new_order_logic
#def get_last_comp_poll(request, pk):


class ServicesCheckViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CheckHead.objects.all()
    serializer_class = CheckHeadSerializer
    model = CheckHead

    def create(self, request):

        logging.warning('create + trololo+ begin' + str(request))
        logging.warning('create + trololo+ begin' + str(request.data))

        meta = request.META
        deviceID = 'TEST'
        if 'HTTP_X_EVOTOR_DEVICE_UUID' in meta:
            deviceID = meta.get('HTTP_X_EVOTOR_DEVICE_UUID')

        logging.warning('create + trololo+ deviceID' + str(deviceID))

        server_data = request.data
        server_data['device_id'] = deviceID

        try:
            check_head = CheckHead.objects.get(uuid=server_data['uuid'])
            check_head.delete()
        except self.model.DoesNotExist:
            pass

        serializer = self.serializer_class(data=server_data)



        if serializer.is_valid():
            serializer.save()

            run_new_order_logic()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=407)





