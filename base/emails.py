from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from main import settings


def send_complaint_email(admin_email, user_email, complaint):
    """Send a complaint confirmation email to the user."""
    context = {
        "user": user_email,
        "complaint": complaint,
    }
    send_mail(
        "Complaint Has Been Sent To You. Please Check Your Complaint On The System",
        f"{complaint}.",
        settings.EMAIL_HOST_USER,
        [admin_email],
        fail_silently=False,
    )
    # Render text and HTML versions of the email
    text_content = render_to_string("emails/complaint_email.txt", context)
    html_content = render_to_string("emails/complaint_email.html", context)

    # Create email message
    msg = EmailMultiAlternatives(
        subject="Your Complaint Has Been Received",
        body=text_content,
        from_email="sanymtechs@gmail.com",
        to=[user_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_notification_email(member_email, message, date, location,name):
    """Send a complaint confirmation email to the user."""
    context = {
        "user": member_email,
        "description": message,
        "date": date,
        "location": location,
        "name": name
    }

    # Render text and HTML versions of the email
    html_content = render_to_string("emails/notification_email.html", context)

    # Create email message
    msg = EmailMultiAlternatives(
        subject=name,
        body=message,
        from_email="sanymtechs@gmail.com",
        to=[member_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()