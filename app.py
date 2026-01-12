"""
@author: Milton Jaramillo  
@since: 07-04-2025  
@summary: API refactorizada con Clean Architecture para el reto técnico de MELI.
          Esta versión implementa una separación clara de responsabilidades con:
          - Domain: Entidades y reglas de negocio puras
          - Application: Casos de uso y lógica de aplicación
          - Infrastructure: Implementaciones concretas (DB, APIs externas, Email)
          - Presentation: Controladores Flask y rutas HTTP
          
          ¡Vamos Milton! MELI es solo el comienzo :)
"""
from flask import Flask
from flask_cors import CORS  # ⭐ AGREGAR ESTE IMPORT
from flasgger import Swagger
from dotenv import load_dotenv
import os

# Infrastructure
from infrastructure.config.settings import Settings
from infrastructure.database.connection import db_connection
from infrastructure.database.models.notification_model import NotificationModel
from infrastructure.repositories.notification_repository_impl import NotificationRepositoryImpl
from infrastructure.external_services.weather_api_service import WeatherAPIService
from infrastructure.external_services.email_service import EmailService

# Application
from application.use_cases.check_weather_use_case import CheckWeatherUseCase
from application.use_cases.get_notifications_use_case import GetNotificationsUseCase

# Presentation
from presentation.routes.weather_routes import WeatherRoutes


def create_app() -> Flask:
    """
    Factory function para crear y configurar la aplicación Flask
    con todas las dependencias inyectadas según Clean Architecture
    """
    # Cargar variables de entorno
    load_dotenv()
    
    # Cargar configuración
    settings = Settings.from_env()
    
    # Inicializar base de datos
    db_connection.initialize_tables([NotificationModel])
    
    # Crear app Flask
    app = Flask(__name__)
    
    # ⭐⭐⭐ CONFIGURAR CORS ⭐⭐⭐
    CORS(app, resources={
        r"/*": {
            "origins": "*",  # En producción, especifica tu dominio
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "x-api-key"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False
        }
    })
    # ⭐⭐⭐ FIN CONFIGURACIÓN CORS ⭐⭐⭐
    
    # Configurar Swagger
    swagger = Swagger(app, template={
        "info": {
            "title": "Weather Alert API - Clean Architecture",
            "description": "API para alertas climáticas con arquitectura limpia",
            "version": "2.0.0",
            "contact": {
                "name": "Milton Jaramillo",
                "email": "milton@example.com"
            }
        },
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "x-api-key"
            }
        },
        "security": [
            {"ApiKeyAuth": []}
        ]
    })
    
    # ===== DEPENDENCY INJECTION =====
    # Infrastructure Layer
    notification_repository = NotificationRepositoryImpl()
    weather_service = WeatherAPIService(
        api_key=settings.WEATHER_API_KEY,
        api_url=settings.WEATHER_API_URL,
        days=settings.WEATHER_DAYS
    )
    email_service = EmailService(
        server=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
        use_tls=settings.MAIL_USE_TLS
    )
    
    # Application Layer - Use Cases
    check_weather_use_case = CheckWeatherUseCase(
        notification_repository=notification_repository,
        weather_service=weather_service,
        email_service=email_service
    )
    get_notifications_use_case = GetNotificationsUseCase(
        notification_repository=notification_repository
    )
    
    # Presentation Layer - Routes
    weather_routes = WeatherRoutes(
        check_weather_use_case=check_weather_use_case,
        get_notifications_use_case=get_notifications_use_case
    )
    
    # Registrar blueprints
    app.register_blueprint(weather_routes.get_blueprint())
    
    return app


# Crear aplicación
app = create_app()


# Correr la app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)