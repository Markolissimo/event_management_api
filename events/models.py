from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class Event(models.Model):
    """
    Model representing an event.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(validators=[MinValueValidator(timezone.now)])
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['location']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self) -> str:
        """
        Return a string representation of the event.
        """
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def available_seats(self) -> int:
        """
        Return the number of available seats for the event.
        """
        return self.capacity - self.registrations.count()

    def is_registration_open(self) -> bool:
        """
        Return True if the registration is open for the event.
        """
        return self.is_active and self.date > timezone.now()

class EventRegistration(models.Model):
    """
    Model representing an event registration.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registration_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self) -> str:
        """
        Return a string representation of the event registration.
        """
        return f"{self.user.email} - {self.event.title}" 