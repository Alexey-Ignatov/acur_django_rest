from acur_research import views

from django.urls import path, include

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'checkheaders', views.CheckHeaderViewSet)
router.register(r'checkpos', views.CheckPosViewSet)

urlpatterns = [
    path('checklist/', views.check_list_simple),
    path('checkneedpoll/<str:pk>/', views.need_poll),
    path('', include(router.urls))
]

