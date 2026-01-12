"""
Swagger Schemas - Capa de Presentación
Definiciones de esquemas para la documentación Swagger
"""


CHECK_WEATHER_SCHEMA = {
    'tags': ['Weather'],
    'description': """
        Este endpoint recibe una ubicación geográfica (latitud y longitud) y una dirección de correo electrónico.  
        Consulta el clima actual y si se detecta mal tiempo (lluvia fuerte, tormentas, etc.), se enviará una alerta al correo proporcionado.  
        Ideal para prevenir riesgos y estar preparado.
    """,
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Clave API de autenticación'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'latitude': {
                        'type': 'number',
                        'example': 5.07,
                        'description': 'Latitud del lugar a consultar'
                    },
                    'longitude': {
                        'type': 'number',
                        'example': -75.52,
                        'description': 'Longitud del lugar a consultar'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'correo@correo.com',
                        'description': 'Correo para recibir alertas'
                    }
                },
                'required': ['latitude', 'longitude', 'email']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Pronóstico exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'forecast': {
                        'type': 'string',
                        'example': 'Soleado con 25°C en Armenia, Colombia'
                    },
                    'location': {
                        'type': 'string',
                        'example': 'Armenia, Colombia'
                    },
                    'adverse_weather': {
                        'type': 'boolean',
                        'example': False
                    },
                    'alert_sent': {
                        'type': 'boolean',
                        'example': False
                    },
                    'message': {
                        'type': 'string',
                        'example': 'No se requiere alerta'
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'latitude, longitude y email son requeridos'
                    }
                }
            }
        },
        401: {
            'description': 'Falta la API key',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'API key requerida'
                    }
                }
            }
        },
        502: {
            'description': 'Error con el servicio externo',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Error al consultar la API del clima'
                    }
                }
            }
        }
    }
}


GET_NOTIFICATIONS_SCHEMA = {
    'tags': ['Weather'],
    'description': """
        Consulta las notificaciones climáticas enviadas previamente a un correo electrónico.  
        Retorna el historial de alertas con información sobre la fecha, condición climática, código de condición y ubicación.  
        Ideal para visualizar el historial de alertas relacionadas al clima que ha recibido un usuario.
    """,
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Clave API de autenticación'
        },
        {
            'name': 'email',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Correo electrónico del usuario que recibió las notificaciones'
        }
    ],
    'responses': {
        200: {
            'description': 'Historial de notificaciones encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'notifications': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'sent_at': {'type': 'string', 'example': '2025-04-07 10:00:00'},
                                'latitude': {'type': 'number', 'example': 5.07},
                                'longitude': {'type': 'number', 'example': -75.52},
                                'condition': {'type': 'string', 'example': 'Heavy Rain'},
                                'code': {'type': 'integer', 'example': 1195}
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Falta el parámetro email',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'El parámetro email es requerido'}
                }
            }
        },
        401: {
            'description': 'Falta la API key',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'API key requerida'}
                }
            }
        },
        404: {
            'description': 'No se encontraron notificaciones',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'No se encontraron notificaciones para correo@ejemplo.com'}
                }
            }
        }
    }
}
