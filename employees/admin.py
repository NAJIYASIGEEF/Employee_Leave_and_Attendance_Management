from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'first_name',
        'last_name',
        'department',
        'designation',
        'manager',
        'employment_status',
    )

    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
    )

    list_filter = (
        'department',
        'employment_status',
    )

    ordering = ('employee_id',)

    date_hierarchy = 'joining_date'

    fieldsets = (
        ('Account Information', {
            'fields': ('user',)
        }),

        ('Personal Information', {
            'fields': (
                'employee_id',
                'first_name',
                'last_name',
                'phone',
            )
        }),

        ('Employment Information', {
            'fields': (
                'joining_date',
                'department',
                'designation',
                'manager',
                'employment_status',
            )
        }),
    )