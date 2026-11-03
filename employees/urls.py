
from django.urls import path
from .views import employee_list,employee_detail

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('<int:id>/', employee_detail, name='employee_detail'),
]
