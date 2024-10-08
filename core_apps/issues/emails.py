import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL  # Import settings for site name and default email

from .models import Issue  # Import the Issue model

# Set up logger for error tracking
logger = logging.getLogger(__name__)

# Function to send an email confirming an issue report
def send_issue_confirmation_email(issue: Issue) -> None:
    """
    Sends a confirmation email to the user who reported the issue.
    """
    try:
        subject = "Issue Report Confirmation"  # Set the email subject
        context = {"issue": issue, "site_name": SITE_NAME}  # Define the context for the email template
        html_email = render_to_string("emails/issue_confirmation.html", context)  # Render the HTML email template
        text_email = strip_tags(html_email)  # Extract plain text from the HTML email
        from_email = DEFAULT_FROM_EMAIL  # Get the default email address from settings
        to = [issue.reported_by.email]  # Set the recipient of the email
        email = EmailMultiAlternatives(subject, text_email, from_email, to)  # Create the email object

        email.attach_alternative(html_email, "text/html")  # Attach the HTML version of the email
        email.send()  # Send the email
    except Exception as e:
        logger.error(
            f"Failed to send confirmation email for issue '{issue.title}':{e}",  # Log the error
            exc_info=True,
        )

# Function to send an email notifying the user that their issue has been resolved
def send_issue_resolved_email(issue: Issue) -> None:
    """
    Sends an email to the user who reported the issue, notifying them that it has been resolved.
    """
    try:
        subject = "Issue Resolved"  # Set the email subject
        context = {"issue": issue, "site_name": SITE_NAME}  # Define the context for the email template
        html_email = render_to_string(
            "emails/issue_resolved_notification.html", context
        )  # Render the HTML email template
        text_email = strip_tags(html_email)  # Extract plain text from the HTML email
        from_email = DEFAULT_FROM_EMAIL  # Get the default email address from settings
        to = [issue.reported_by.email]  # Set the recipient of the email
        email = EmailMultiAlternatives(subject, text_email, from_email, to)  # Create the email object

        email.attach_alternative(html_email, "text/html")  # Attach the HTML version of the email
        email.send()  # Send the email
    except Exception as e:
        logger.error(
            f"Failed to send resolution email for issue '{issue.title}':{e}",  # Log the error
            exc_info=True,
        )

# Function to send an email notifying the user that their issue has been resolved
def send_resolution_email(issue: Issue) -> None:
    """
    Sends an email to the user who reported the issue, notifying them that it has been resolved.
    """
    try:
        subject = f"Issue Resolved: {issue.title}"  # Set the email subject
        from_email = DEFAULT_FROM_EMAIL  # Get the default email address from settings
        recipient_list = [issue.reported_by.email]  # Set the recipient of the email
        context = {"issue": issue, "site_name": SITE_NAME}  # Define the context for the email template
        html_email = render_to_string(
            "emails/issue_resolved_notification.html", context
        )  # Render the HTML email template
        text_email = strip_tags(html_email)  # Extract plain text from the HTML email
        email = EmailMultiAlternatives(
            subject, text_email, from_email, recipient_list
        )  # Create the email object

        email.attach_alternative(html_email, "text/html")  # Attach the HTML version of the email
        email.send()  # Send the email
    except Exception as e:
        logger.error(
            f"Failed to send resolution email for issue '{issue.title}':{e}",  # Log the error
            exc_info=True,
        )