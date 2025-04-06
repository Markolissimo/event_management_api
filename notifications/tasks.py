from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from events.models import Event, EventRegistration

User = get_user_model()

@shared_task
def send_event_registration_email(user_id: int, event_id: int, registration_id: int) -> None:
    """
    Send an email to the user when they register for an event.
    """
    try:
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        registration = EventRegistration.objects.get(id=registration_id)

        subject = f'Event Registration Confirmation: {event.title}'
        message = render_to_string('emails/event_registration.html', {
            'user': user,
            'event': event,
            'registration': registration,
        })

        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending registration email: {str(e)}")
        raise 