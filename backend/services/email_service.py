from __future__ import annotations
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.config import settings


def _enviar_smtp(email: str, msg: MIMEMultipart) -> None:
    """Intenta puerto 465 (SSL) primero, luego 587 (STARTTLS) como fallback."""
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        raise RuntimeError("SMTP_EMAIL o SMTP_PASSWORD no configurados en las variables de entorno")

    ctx = ssl.create_default_context()

    # Intento 1: Puerto 465 SSL directo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=30) as server:
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, email, msg.as_string())
        return
    except Exception:
        pass

    # Intento 2: Puerto 587 STARTTLS
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.ehlo()
        server.starttls(context=ctx)
        server.ehlo()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_EMAIL, email, msg.as_string())


def enviar_codigo_verificacion(email: str, nombre: str, codigo: str) -> None:
    html = f"""
    <div style="font-family:Arial,sans-serif;background:#060e0a;padding:2rem;max-width:480px;
                margin:0 auto;border-radius:16px;border:1px solid #00d47a">
      <h2 style="color:#00d47a;margin:0 0 .5rem">Santa Cruz Segura Predictiva</h2>
      <p style="color:#94a3b8;font-size:15px">Hola <b style="color:#f1f5f9">{nombre}</b>, gracias por registrarte.</p>
      <p style="color:#94a3b8;font-size:15px">Tu código de verificación es:</p>
      <div style="background:#0f1f14;border:2px solid #00d47a;border-radius:12px;
                  padding:20px;margin:16px 0;text-align:center">
        <span style="font-size:36px;font-weight:900;letter-spacing:12px;color:#00d47a">{codigo}</span>
      </div>
      <p style="color:#475569;font-size:13px">
        Ingresa este código en la pantalla de verificación.<br>
        Válido por 24 horas. Si no creaste esta cuenta, ignora este mensaje.
      </p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Código de verificación: {codigo} — Santa Cruz Segura"
    msg["From"] = f"Santa Cruz Segura <{settings.SMTP_EMAIL}>"
    msg["To"] = email
    msg.attach(MIMEText(html, "html", "utf-8"))

    _enviar_smtp(email, msg)
