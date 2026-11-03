
# Create your views here.

from django.shortcuts import render
from .models import Employee


def employee_list(request):
    employees = Employee.objects.select_related(
        'department', 'user'
    ).all()

    return render(
        request,
        'employees/employee_list.html',
        {'employees': employees}
    )
