import smtplib
from email.mime.text import MIMEText
import os

from app.config import get_config


def send_group_invitation_email(
    recipient_email: str,
    inviter_name: str,
    group_name: str,
    invite_link: str,
):
    config = get_config()
    gmail_user = os.getenv("GMAIL_USER") or config.get("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD") or config.get("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_app_password:
        raise RuntimeError("Gmail SMTP credentials are not configured")

    html = f"""
    <h2>You're invited!</h2>
    <p><strong>{inviter_name}</strong> invited you to join <strong>{group_name}</strong>.</p>
    <a href="{invite_link}">Join Group</a>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = f"{inviter_name} invited you to join {group_name}"
    msg["From"] = gmail_user
    msg["To"] = recipient_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_app_password)
        smtp.send_message(msg)
