from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from typing import Any


def send_email_notification(subject: str, template_name: str, context: dict, recipient_list: list) -> None:
    """
    Send an email notification using a template.
    
    Args:
        subject (str): Email subject
        template_name (str): Name of the template file
        context (dict): Context data for the template
        recipient_list (list): List of email recipients
    """
    message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message='',
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


def get_file_upload_path(instance: Any, filename: str) -> str:
    """
    Generate a unique file path for uploaded files.
    
    Args:
        instance: The model instance
        filename (str): Original filename
    
    Returns:
        str: Generated file path
    """
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{instance._meta.model_name}/{timestamp}.{ext}'


def format_date_range(start_date: datetime, end_date: datetime) -> str:
    """
    Format a date range in a human-readable format.
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
    
    Returns:
        str: Formatted date range
    """
    if start_date.date() == end_date.date():
        return f"{start_date.strftime('%B %d, %Y')} {start_date.strftime('%I:%M %p')} - {end_date.strftime('%I:%M %p')}"
    return f"{start_date.strftime('%B %d, %Y %I:%M %p')} - {end_date.strftime('%B %d, %Y %I:%M %p')}" 