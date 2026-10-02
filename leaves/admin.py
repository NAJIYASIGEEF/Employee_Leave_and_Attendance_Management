from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'max_days',
        'is_paid',
        'is_active',
    )

    search_fields = ('name',)

    list_filter = (
        'is_paid',
        'is_active',
    )


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'leave_type',
        'year',
        'allocated_days',
        'used_days',
        'remaining_days',
    )

    search_fields = (
        'employee__employee_id',
        'employee__first_name',
        'employee__last_name',
    )

    list_filter = (
        'year',
        'leave_type',
    )


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'leave_type',
        'start_date',
        'end_date',
        'number_of_days',
        'status',
    )

    search_fields = (
        'employee__employee_id',
        'employee__first_name',
        'employee__last_name',
    )

    list_filter = (
        'status',
        'leave_type',
    )
    
