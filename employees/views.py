
# Create your views here.

from django.shortcuts import render , get_object_or_404
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




def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)

    return render(
        request,
        'employees/employee_detail.html',
        {'employee': employee}
    )
