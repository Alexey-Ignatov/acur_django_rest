from acur_research import views

from django.urls import path

urlpatterns = [
    path('checklist/', views.check_list_simple),

]
