"""
Weather Routes - Capa de Presentación
Definición de las rutas HTTP para las funcionalidades de clima
"""
from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from presentation.middlewares.auth_middleware import require_api_key
from presentation.schemas.swagger_schemas import CHECK_WEATHER_SCHEMA, GET_NOTIFICATIONS_SCHEMA
from application.use_cases.check_weather_use_case import CheckWeatherUseCase
from application.use_cases.get_notifications_use_case import GetNotificationsUseCase
from application.dto.weather_request_dto import WeatherRequestDTO
from infrastructure.external_services.weather_api_service import WeatherAPIException
from infrastructure.external_services.email_service import EmailException


class WeatherRoutes:
    """Clase que define las rutas del módulo de clima"""
    
    def __init__(
        self,
        check_weather_use_case: CheckWeatherUseCase,
        get_notifications_use_case: GetNotificationsUseCase
    ):
        self.check_weather_use_case = check_weather_use_case
        self.get_notifications_use_case = get_notifications_use_case
        self.blueprint = Blueprint('weather', __name__)
        self._register_routes()
    
    def _register_routes(self):
        """Registra todas las rutas del blueprint"""
        
        @self.blueprint.route('/check_weather', methods=['POST'])
        @swag_from(CHECK_WEATHER_SCHEMA)
        @require_api_key
        def check_weather():
            """Endpoint para verificar el clima y enviar alertas"""
            try:
                data = request.get_json()
                
                # Validar datos requeridos
                if not data:
                    return jsonify({'error': 'Body requerido'}), 400
                
                lat = data.get('latitude')
                lon = data.get('longitude')
                email = data.get('email')
                
                if lat is None or lon is None or not email:
                    return jsonify({'error': 'latitude, longitude y email son requeridos'}), 400
                
                # Crear DTO y ejecutar caso de uso
                weather_request = WeatherRequestDTO(
                    latitude=float(lat),
                    longitude=float(lon),
                    email=email
                )
                
                result = self.check_weather_use_case.execute(weather_request)
                return jsonify(result), 200
                
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except WeatherAPIException as e:
                return jsonify({'error': str(e)}), 502
            except EmailException as e:
                return jsonify({'error': f'Error al enviar email: {str(e)}'}), 500
            except Exception as e:
                return jsonify({'error': f'Error interno: {str(e)}'}), 500
        
        @self.blueprint.route('/notifications', methods=['GET'])
        @swag_from(GET_NOTIFICATIONS_SCHEMA)
        @require_api_key
        def get_notifications():
            """Endpoint para obtener el historial de notificaciones"""
            try:
                email = request.args.get('email')
                
                if not email:
                    return jsonify({'error': 'El parámetro email es requerido'}), 400
                
                # Ejecutar caso de uso
                result = self.get_notifications_use_case.execute(email)
                
                # Verificar si hay notificaciones
                if not result.notifications:
                    return jsonify({'message': f'No se encontraron notificaciones para {email}'}), 404
                
                return jsonify(result.to_dict()), 200
                
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return jsonify({'error': f'Error interno: {str(e)}'}), 500
    
    def get_blueprint(self) -> Blueprint:
        """Retorna el blueprint configurado"""
        return self.blueprint
