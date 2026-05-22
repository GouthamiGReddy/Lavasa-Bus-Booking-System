from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('5', '5th Year'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def is_student(self):
        return self.role == 'student'

    def is_faculty(self):
        return self.role == 'faculty'


class BusSlot(models.Model):
    SERVICE_CHOICES = [
        ('weekend', 'Weekend Bus Service'),
        ('vacation', 'Vacation Bus Service'),
    ]
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, default='weekend')
    date = models.DateField()
    departure_time = models.TimeField()
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField(default=45)
    description = models.TextField(blank=True)

    # For weekend service: merged return slot
    has_return = models.BooleanField(default=False)
    return_time = models.TimeField(null=True, blank=True)
    return_from = models.CharField(max_length=100, blank=True)
    return_to = models.CharField(max_length=100, blank=True)
    return_seats = models.PositiveIntegerField(default=45)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def available_seats(self):
        booked = self.bookings.filter(
            status__in=['pending', 'approved'],
            journey_type__in=['oneway', 'bothway']
        ).count()
        return self.total_seats - booked

    def available_return_seats(self):
        if not self.has_return:
            return 0
        booked = self.bookings.filter(
            status__in=['pending', 'approved'],
            journey_type='bothway'
        ).count()
        # Also count return-only bookings if any (not applicable in current flow)
        return self.return_seats - booked

    def __str__(self):
        return f"{self.service_type.upper()} | {self.date} | {self.from_location} → {self.to_location} @ {self.departure_time}"

    class Meta:
        ordering = ['date', 'departure_time']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ]
    JOURNEY_CHOICES = [
        ('oneway', 'One Way'),
        ('bothway', 'Both Ways'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(BusSlot, on_delete=models.CASCADE, related_name='bookings')
    journey_type = models.CharField(max_length=10, choices=JOURNEY_CHOICES, default='oneway')
    reason = models.TextField(blank=True)
    proof = models.FileField(upload_to='proofs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    admin_note = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'slot')
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user.username} - {self.slot} ({self.status})"
