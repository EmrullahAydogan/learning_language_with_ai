"""
Email service for sending verification, notification, and reminder emails
"""

from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from pathlib import Path
from jinja2 import Template
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email service using SMTP"""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
        self.templates_dir = Path(__file__).parent.parent / "templates" / "emails"

    def _get_smtp_connection(self):
        """Get SMTP connection"""
        try:
            if settings.SMTP_TLS:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)

            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)

            return server
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            raise

    def _render_template(self, template_name: str, context: dict) -> str:
        """Render email template"""
        template_path = self.templates_dir / f"{template_name}.html"

        if not template_path.exists():
            # Return plain text if template doesn't exist
            logger.warning(f"Email template not found: {template_name}")
            return context.get("message", "")

        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        template = Template(template_content)
        return template.render(**context)

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email"""
        if not settings.EMAILS_ENABLED:
            logger.info(f"Emails disabled. Would send to {to_email}: {subject}")
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            # Add text part
            if text_content:
                part1 = MIMEText(text_content, "plain")
                msg.attach(part1)

            # Add HTML part
            part2 = MIMEText(html_content, "html")
            msg.attach(part2)

            # Send email
            with self._get_smtp_connection() as server:
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    def send_verification_email(self, to_email: str, username: str, verification_token: str) -> bool:
        """Send email verification"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"

        context = {
            "username": username,
            "verification_url": verification_url,
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("verification", context)
        subject = "Verify Your Email - Language Learning Platform"

        return self.send_email(to_email, subject, html_content)

    def send_password_reset_email(self, to_email: str, username: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        context = {
            "username": username,
            "reset_url": reset_url,
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("password_reset", context)
        subject = "Reset Your Password - Language Learning Platform"

        return self.send_email(to_email, subject, html_content)

    def send_welcome_email(self, to_email: str, username: str) -> bool:
        """Send welcome email after verification"""
        context = {
            "username": username,
            "dashboard_url": f"{settings.FRONTEND_URL}/dashboard",
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("welcome", context)
        subject = "Welcome to Language Learning Platform!"

        return self.send_email(to_email, subject, html_content)

    def send_daily_reminder_email(
        self,
        to_email: str,
        username: str,
        current_streak: int,
        daily_goal_progress: int
    ) -> bool:
        """Send daily learning reminder"""
        context = {
            "username": username,
            "current_streak": current_streak,
            "daily_goal_progress": daily_goal_progress,
            "dashboard_url": f"{settings.FRONTEND_URL}/dashboard",
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("daily_reminder", context)
        subject = f"Don't break your {current_streak}-day streak! 🔥"

        return self.send_email(to_email, subject, html_content)

    def send_achievement_email(
        self,
        to_email: str,
        username: str,
        achievement_name: str,
        achievement_description: str
    ) -> bool:
        """Send achievement unlocked email"""
        context = {
            "username": username,
            "achievement_name": achievement_name,
            "achievement_description": achievement_description,
            "progress_url": f"{settings.FRONTEND_URL}/progress",
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("achievement", context)
        subject = f"Achievement Unlocked: {achievement_name} 🏆"

        return self.send_email(to_email, subject, html_content)

    def send_level_up_email(
        self,
        to_email: str,
        username: str,
        new_level: int,
        language: str
    ) -> bool:
        """Send level up congratulations email"""
        context = {
            "username": username,
            "new_level": new_level,
            "language": language,
            "progress_url": f"{settings.FRONTEND_URL}/progress",
            "app_name": "Language Learning Platform"
        }

        html_content = self._render_template("level_up", context)
        subject = f"Level Up! You're now Level {new_level} in {language} 🎉"

        return self.send_email(to_email, subject, html_content)


# Singleton instance
email_service = EmailService()
