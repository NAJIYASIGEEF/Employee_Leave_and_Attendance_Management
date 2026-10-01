
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    EMPLOYMENT_STATUS = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

# User → Employee
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
        
        
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=15, blank=True)

    joining_date = models.DateField()

#Department → Employees

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='employees'
    )

    designation = models.CharField(max_length=100)

# Manager → Team members
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS,
        default='ACTIVE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

def clean(self):
    if self.joining_date and self.joining_date > timezone.localdate():
        raise ValidationError({
            'joining_date': 'Joining date cannot be in the future.'
        })

    if self.manager and self.manager == self:
        raise ValidationError({
            'manager': 'An employee cannot be their own manager.'
        })

def __str__(self):
    return f"{self.employee_id} - {self.first_name}"