"""
Auth Middleware - Capa de Presentación
Middleware para autenticación con API Key
"""
from functools import wraps
from flask import request, jsonify
from infrastructure.config.settings import Settings


def require_api_key(f):
    """
    Decorador que requiere una API key válida en el header
    
    Usage:
        @require_api_key
        def my_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        settings = Settings.from_env()
        
        if not api_key:
            return jsonify({'error': 'API key requerida'}), 401
        
        if api_key != settings.API_KEY:
            return jsonify({'error': 'API key inválida'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
