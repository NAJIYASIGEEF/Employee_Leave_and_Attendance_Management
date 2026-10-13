from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest
from django.db import transaction
from django.core.exceptions import ValidationError


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
    


  
    def save_model(self, request, obj, form, change):
        from django.db import transaction
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        with transaction.atomic():
            old_obj = None

            if change:
                old_obj = LeaveRequest.objects.get(pk=obj.pk)

            old_status = old_obj.status if old_obj else None

            # Restore balance if an approved request is rejected or cancelled.
            if (
                old_obj
                and old_status == 'APPROVED'
                and obj.status in ['REJECTED', 'CANCELLED']
            ):
                old_year = old_obj.start_date.year

                old_balance = LeaveBalance.objects.select_for_update().filter(
                    employee=old_obj.employee,
                    leave_type=old_obj.leave_type,
                    year=old_year
                ).first()

                if not old_balance:
                    raise ValidationError(
                        'Leave balance not found for the approved request.'
                    )

                old_balance.used_days -= old_obj.number_of_days

                if old_balance.used_days < 0:
                    raise ValidationError(
                        'Leave balance cannot have negative used days.'
                    )

                old_balance.save()

            # Deduct balance when a request becomes approved.
            if obj.status == 'APPROVED' and old_status != 'APPROVED':
                year = obj.start_date.year

                balance = LeaveBalance.objects.select_for_update().filter(
                    employee=obj.employee,
                    leave_type=obj.leave_type,
                    year=year
                ).first()

                if not balance:
                    raise ValidationError(
                        'Leave balance not found for this employee, leave type, and year.'
                    )

                if balance.remaining_days < obj.number_of_days:
                    raise ValidationError(
                        'Insufficient leave balance to approve this request.'
                    )

                balance.used_days += obj.number_of_days
                balance.save()

                obj.approved_by = getattr(request.user, 'employee', None)
                obj.approved_at = timezone.now()

            super().save_model(request, obj, form, change)
