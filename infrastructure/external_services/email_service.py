"""
Email Service - Capa de Infraestructura
Servicio para enviar correos electrónicos
"""
import os
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailException(Exception):
    """Excepción personalizada para errores de email"""
    pass


def force_ipv4():
    """
    Fuerza a Python a usar IPv4 en lugar de IPv6.
    Necesario en algunos entornos cloud (como Render) donde IPv6 no tiene ruta.
    """
    original_getaddrinfo = socket.getaddrinfo

    def ipv4_first(*args, **kwargs):
        results = original_getaddrinfo(*args, **kwargs)
        ipv4 = [r for r in results if r[0] == socket.AF_INET]
        return ipv4 if ipv4 else results

    socket.getaddrinfo = ipv4_first


class EmailService:
    """Servicio para enviar correos electrónicos usando SMTP"""

    def __init__(
        self,
        server: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = True
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

        # 🔴 IMPORTANTE:
        # Forzamos IPv4 solo cuando estamos en Render
        if os.getenv("RENDER", "").lower() in ("1", "true", "yes"):
            force_ipv4()

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Envía un correo electrónico
        """
        try:
            message = MIMEMultipart()
            message["From"] = self.username
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(self.server, self.port, timeout=20) as server:
                server.ehlo()

                if self.use_tls:
                    server.starttls()
                    server.ehlo()

                server.login(self.username, self.password)
                server.send_message(message)

        except (smtplib.SMTPException, OSError) as e:
            # OSError captura errores de red como: [Errno 101] Network is unreachable
            raise EmailException(f"Error al enviar el correo: {e}")

        except Exception as e:
            raise EmailException(f"Error inesperado al enviar el correo: {e}")
