from __future__ import annotations
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.config import settings


def enviar_codigo_verificacion(email: str, nombre: str, codigo: str) -> None:
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        return

    html = f"""
    <div style="font-family:Inter,sans-serif;background:#060e0a;padding:2rem;max-width:480px;margin:0 auto;border-radius:16px;border:1px solid rgba(0,212,122,.2)">
      <h2 style="color:#00d47a;margin-bottom:.5rem">Santa Cruz Segura Predictiva</h2>
      <p style="color:#94a3b8;font-size:.9rem">Hola <b style="color:#f1f5f9">{nombre}</b>, gracias por registrarte.</p>
      <p style="color:#94a3b8;font-size:.9rem">Tu código de verificación es:</p>
      <div style="background:#0f1f14;border:2px solid #00d47a;border-radius:12px;padding:1.2rem 2rem;margin:1rem 0;text-align:center">
        <span style="font-size:2.2rem;font-weight:900;letter-spacing:.4rem;color:#00d47a">{codigo}</span>
      </div>
      <p style="color:#475569;font-size:.78rem">Ingresa este código en la pantalla de verificación.<br>Válido por 24 horas. Si no creaste esta cuenta, ignora este mensaje.</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Tu código de verificación: {codigo} — Santa Cruz Segura"
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_EMAIL, email, msg.as_string())
