"""
Email Service - Capa de Infraestructura
Servicio para enviar correos electrónicos
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailException(Exception):
    """Excepción personalizada para errores de email"""
    pass


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
    
    def send_email(self, to_email: str, subject: str, body: str):
        """
        Envía un correo electrónico
        
        Args:
            to_email: Dirección de correo del destinatario
            subject: Asunto del correo
            body: Cuerpo del correo
            
        Raises:
            EmailException: Si hay un error al enviar el correo
        """
        try:
            # Crear mensaje
            message = MIMEMultipart()
            message['From'] = self.username
            message['To'] = to_email
            message['Subject'] = subject
            
            # Agregar cuerpo del mensaje
            message.attach(MIMEText(body, 'plain'))
            
            # Conectar al servidor SMTP y enviar
            with smtplib.SMTP(self.server, self.port) as server:
                if self.use_tls:
                    server.starttls()
                
                server.login(self.username, self.password)
                server.send_message(message)
                
        except smtplib.SMTPException as e:
            raise EmailException(f"Error al enviar el correo: {str(e)}")
        except Exception as e:
            raise EmailException(f"Error inesperado al enviar el correo: {str(e)}")
