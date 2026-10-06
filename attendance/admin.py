from django.contrib import admin
from django import forms
from .models import Attendance


class AttendanceAdminForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'

        widgets = {
            'check_in': forms.TimeInput(
                format='%I:%M %p',
                attrs={'placeholder': '09:30 AM'}
            ),
            'check_out': forms.TimeInput(
                format='%I:%M %p',
                attrs={'placeholder': '06:00 PM'}
            ),
        }


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm

    list_display = (
        'employee',
        'date',
        'check_in',
        'check_out',
        'status',
    )

    search_fields = (
        'employee__employee_id',
        'employee__first_name',
        'employee__last_name',
    )

    list_filter = (
        'status',
        'date',
    )

    ordering = ('-date',)