from __future__ import annotations
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.config import settings


def enviar_verificacion(email: str, nombre: str, token: str) -> None:
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        return

    link = f"{settings.APP_URL}/auth/verificar/{token}"

    html = f"""
    <div style="font-family:Inter,sans-serif;background:#060e0a;padding:2rem;max-width:480px;margin:0 auto;border-radius:16px;border:1px solid rgba(0,212,122,.2)">
      <h2 style="color:#00d47a;margin-bottom:.5rem">Santa Cruz Segura Predictiva</h2>
      <p style="color:#94a3b8;font-size:.9rem">Hola <b style="color:#f1f5f9">{nombre}</b>, gracias por registrarte.</p>
      <p style="color:#94a3b8;font-size:.9rem">Confirma tu correo haciendo clic en el botón:</p>
      <a href="{link}" style="display:inline-block;margin:1rem 0;background:#00d47a;color:#060e0a;font-weight:700;padding:.75rem 1.5rem;border-radius:10px;text-decoration:none;font-size:.9rem">
        Verificar mi correo
      </a>
      <p style="color:#475569;font-size:.78rem">Este enlace expira en 24 horas.<br>Si no creaste esta cuenta, ignora este mensaje.</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verifica tu correo — Santa Cruz Segura"
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_EMAIL, email, msg.as_string())
