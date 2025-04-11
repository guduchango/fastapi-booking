from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from jinja2 import Template
from typing import Dict, Any
import os

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "mailhog")
        self.smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "reservations@example.com")

    async def send_email(self, to_email: str, subject: str, template_name: str, context: Dict[str, Any]):
        """Send an email using a template."""
        # Load email template
        template_path = os.path.join(os.path.dirname(__file__), "templates", f"{template_name}.html")
        with open(template_path, "r") as f:
            template = Template(f.read())
        
        # Render template with context
        html_content = template.render(**context)

        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject

        # Attach HTML content
        message.attach(MIMEText(html_content, "html"))

        # Send email
        await aiosmtplib.send(
            message,
            hostname=self.smtp_host,
            port=self.smtp_port,
            username=self.smtp_user,
            password=self.smtp_password,
            use_tls=False
        ) 