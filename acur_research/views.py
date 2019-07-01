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

class EvoCloudTokenViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = EvoUser.objects.all()
    serializer_class = EvoUserSerializer


    def create(self, request):
        logging.warning('create + trololo+ begin' + str(request))
        logging.warning('create + trololo+ begin' + str(request.data))


        try:
            evo_user = EvoUser.objects.get(userId=request.data['userId'])
            serializer = self.serializer_class(evo_user, data=request.data)
        except EvoUser.DoesNotExist:
            serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=407)









class PollResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = PollResult.objects.all()
    serializer_class = PollResultSerializer

    def create(self, request):
        #logging.warning('create + trololo+ begin' + str(request))
        logging.warning('create + trololo+ begin' + str(request.data))

        data = json.loads(request.data['data'])
        serializer = PollResultSerializer(data=data['answer'])
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=407)





class CheckHeaderViewSet(viewsets.ModelViewSet):
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
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=407)










@csrf_exempt
def need_poll(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    curr_check = CheckHead.objects.filter(uuid=pk)
    if not curr_check:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if poll_is_needed(curr_check):
            return JsonResponse({'result': True})
        return JsonResponse({'result': False})


@csrf_exempt
def set_phone(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        curr_check = CheckHead.objects.get(uuid=pk)
    except CheckHead.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CheckPhoneNumberSerializer(data=data)
        if serializer.is_valid():
            phone_obj = serializer.save()
            curr_check.tel_no = phone_obj
            curr_check.save()

            account_sid = 'AC1951c9d363cbfebedd5c43183002c9df'
            auth_token = '06243a6dccddc70b95461ce3bd326612'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body="https://anketolog.ru/s/245974/QGWYwXCh?ap_check=" + curr_check.uuid,
                from_='+12055572693',
                to='+'+ phone_obj.tel_str
            )



            return JsonResponse(CheckHeadSerializer(curr_check).data)
        return JsonResponse(serializer.errors, status=400)









class CheckList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = CheckHead.objects.all()
    serializer_class = CheckHeadSerializer

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




@csrf_exempt
@require_POST
def webhook(request):
    print('rout_new_answer_1')
    data = JSONParser().parse(request)
    serializer = PollResultSerializer(data=data['answer'])
    if serializer.is_valid():
        print('rout_new_answer_valid')
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)




@csrf_exempt
def get_last_some(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """

    meta = request.META
    deviceID = 'TEST'
    if 'HTTP_X_EVOTOR_DEVICE_UUID' in meta:
        deviceID = meta.get('HTTP_X_EVOTOR_DEVICE_UUID')



    all_my_completed = CheckHead.objects.filter(device_id=deviceID, tel_no__isnull = False).order_by('-id')[:int(pk)]

    if request.method == 'GET':
        logging.warning('create + trololo+ begin' + str([l.tel_no.tel_str for l in all_my_completed]))
        resp_data= [l.tel_no.tel_str for l in all_my_completed]
        return JsonResponse(resp_data, safe=False)
    return JsonResponse([], safe=False)



def index(request):
   print('index_trololo')
   return HttpResponse('US37MZnTroVjLpx_53c9TelbGskqRslNf8EgvO_lKWLYTd8I7ufO7Kl053Wp')



#def get_last_comp_poll(request, pk):






