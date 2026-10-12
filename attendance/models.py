from django.db import models
from employees.models import Employee
from django.core.exceptions import ValidationError


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('HALF_DAY', 'Half Day'),
        ('LEAVE', 'Leave'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField()

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def clean(self):
        if (
            self.employee_id
            and self.date
            and self.status in ['PRESENT', 'HALF_DAY']
        ):
            approved_leave = self.employee.leave_requests.filter(
                status='APPROVED',
                start_date__lte=self.date,
                end_date__gte=self.date
            ).exists()

            if approved_leave:
                raise ValidationError(
                    "Attendance cannot be marked for a day with approved leave."
                )

        if self.status in ['ABSENT', 'LEAVE']:
            if self.check_in or self.check_out:
                raise ValidationError(
                    "Check-in and check-out times are not allowed for Absent or Leave."
                )

        if self.check_out and not self.check_in:
            raise ValidationError(
                "Check-in time is required when check-out time is entered."
            )

        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError(
                    "Check-out time must be after check-in time."
                )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'date'],
                name='unique_employee_attendance_date'
            )
        ]

    @property
    def working_hours(self):
        if self.check_in and self.check_out:
            from datetime import datetime

            start = datetime.combine(self.date, self.check_in)
            end = datetime.combine(self.date, self.check_out)

            return end - start

        return None

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date}"