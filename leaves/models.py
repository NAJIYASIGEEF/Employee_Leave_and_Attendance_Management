
from django.db import models
from django.core.exceptions import ValidationError
from employees.models import Employee


# 1. Leave Type Model
class LeaveType(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    max_days = models.PositiveIntegerField()

    is_paid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 2. Leave Balance Model
class LeaveBalance(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='balances'
    )

    year = models.PositiveIntegerField()

    allocated_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def remaining_days(self):
        return self.allocated_days - self.used_days

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type.name} - {self.year}"


# 3. Leave Request Model
class LeaveRequest(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name='leave_requests'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    number_of_days = models.PositiveIntegerField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leave_requests'
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Leave Validation
    def clean(self):

        if self.start_date and self.end_date:

            # Validate date order
            if self.start_date > self.end_date:
                raise ValidationError({
                    'end_date': 'End date cannot be before start date.'
                })

            # Calculate leave duration
            calculated_days = (
                self.end_date - self.start_date
            ).days + 1

            if calculated_days < 1:
                raise ValidationError({
                    'number_of_days': 'Leave must be at least 1 day.'
                })

            self.number_of_days = calculated_days

            # Check overlapping leave requests
            if self.employee_id:

                overlapping_requests = self.employee.leave_requests.filter(
                    status__in=['PENDING', 'APPROVED'],
                    start_date__lte=self.end_date,
                    end_date__gte=self.start_date
                ).exclude(pk=self.pk)

                if overlapping_requests.exists():
                    raise ValidationError({
                        'start_date': 'You already have a leave request for these dates.'
                    })

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type.name} - {self.status}"