from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from acur_research.serializers import CheckHeadSerializer, CheckPositionSerializer
from acur_research.models import CheckHead, CheckPosition
from rest_framework import mixins
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from acur_research.analytic import poll_is_needed


class CheckHeaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CheckHead.objects.all()
    serializer_class = CheckHeadSerializer




class CheckPosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CheckPosition.objects.all()
    serializer_class = CheckPositionSerializer


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











# Create your views here.
@csrf_exempt
def check_list_simple(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        checks = CheckHead.objects.all()
        serializer = CheckHeadSerializer(checks, many=True)
        return JsonResponse(serializer.data, safe=False)







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