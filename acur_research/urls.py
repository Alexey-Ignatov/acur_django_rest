from acur_research import views

from django.urls import path, include

from rest_framework import routers
from django.conf.urls import include, url
from acur_research.acurservices.views import ServicesCheckViewSet

router = routers.DefaultRouter()
router.register(r'checkheaders', views.CheckHeaderViewSet)
#router.register(r'checkpos', views.CheckPosViewSet)
router.register(r'webhook', views.PollResultViewSet)
router.register(r'evoauthtoken', views.EvoCloudTokenViewSet)
router.register(r'servcheck', views.ServicesCheckViewSet)



urlpatterns = [
    path('checkneedpoll/<str:pk>/', views.need_poll),
    path('setphone/<str:pk>/', views.set_phone),
    path("compl_tels/<int:pk>/", views.get_last_some),
    path('', include(router.urls))
]

#K0ymrcxHKM
