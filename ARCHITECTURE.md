# 🏗️ Documentación de Arquitectura - Clean Architecture

## 📋 Índice
1. [Introducción](#introducción)
2. [Principios de Clean Architecture](#principios-de-clean-architecture)
3. [Capas de la Aplicación](#capas-de-la-aplicación)
4. [Flujo de Datos](#flujo-de-datos)
5. [Patrones Implementados](#patrones-implementados)
6. [Decisiones de Diseño](#decisiones-de-diseño)

---

## Introducción

Este proyecto implementa **Clean Architecture** (Arquitectura Limpia), un patrón arquitectónico propuesto por Robert C. Martin (Uncle Bob) que promueve la separación de responsabilidades y la independencia de frameworks, bases de datos y servicios externos.

### ¿Por qué Clean Architecture?

- ✅ **Independencia del Framework**: La lógica de negocio no depende de Flask
- ✅ **Testabilidad**: Cada componente puede ser testeado de forma aislada
- ✅ **Independencia de la UI**: Puedes cambiar de REST API a GraphQL sin tocar la lógica
- ✅ **Independencia de la Base de Datos**: Puedes cambiar de SQLite a PostgreSQL fácilmente
- ✅ **Independencia de Servicios Externos**: Cambiar de WeatherAPI a otra API es simple

---

## Principios de Clean Architecture

### 1. Regla de Dependencia

**Las dependencias solo pueden apuntar hacia adentro.**

```
Presentation → Application → Domain
    ↓              ↓
Infrastructure
```

- **Domain** no depende de nada
- **Application** solo depende de Domain
- **Infrastructure** implementa interfaces definidas en Domain
- **Presentation** usa Application y coordina todo

### 2. Inversión de Dependencias

En lugar de que la lógica de negocio dependa de implementaciones concretas:

```python
# ❌ Mal - Dependencia directa
class CheckWeatherUseCase:
    def __init__(self):
        self.repo = NotificationRepositoryImpl()  # Acoplamiento
```

Usamos interfaces:

```python
# ✅ Bien - Inversión de dependencias
class CheckWeatherUseCase:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository  # Interfaz
```

### 3. Entidades vs Casos de Uso

- **Entidades** (Domain): Reglas de negocio puras, aplicables en cualquier contexto
- **Casos de Uso** (Application): Reglas específicas de esta aplicación

---

## Capas de la Aplicación

### 🟢 1. Domain (Capa de Dominio)

**Responsabilidad**: Contiene las reglas de negocio puras y entidades.

**Características**:
- Sin dependencias externas
- Sin imports de frameworks
- Código que podría vivir en cualquier aplicación

**Contenido**:

```
domain/
├── entities/
│   ├── forecast.py          # Entidad Pronóstico del Clima
│   └── notification.py      # Entidad Notificación
└── repositories/
    └── notification_repository.py  # Interfaz del repositorio
```

**Ejemplo - Entidad Forecast**:
```python
@dataclass
class Forecast:
    location: str
    temperature_c: float
    condition: str
    is_adverse: bool
    
    def requires_alert(self) -> bool:
        """Lógica de negocio pura"""
        return self.is_adverse
```

---

### 🔵 2. Application (Capa de Aplicación)

**Responsabilidad**: Contiene los casos de uso y la lógica específica de la aplicación.

**Características**:
- Orquesta el flujo de datos
- No conoce detalles de implementación (DB, HTTP, etc.)
- Solo depende de la capa Domain

**Contenido**:

```
application/
├── use_cases/
│   ├── check_weather_use_case.py      # Caso de uso: Verificar clima
│   └── get_notifications_use_case.py  # Caso de uso: Obtener notificaciones
└── dto/
    ├── weather_request_dto.py         # DTO de entrada
    └── notification_dto.py            # DTO de salida
```

**Ejemplo - Use Case**:
```python
class CheckWeatherUseCase:
    def __init__(
        self,
        notification_repository: NotificationRepository,  # Interfaz
        weather_service,                                   # Inyectado
        email_service                                      # Inyectado
    ):
        self.notification_repository = notification_repository
        self.weather_service = weather_service
        self.email_service = email_service
    
    def execute(self, request: WeatherRequestDTO) -> dict:
        # 1. Validar
        # 2. Obtener forecast
        # 3. Si es adverso, enviar alerta
        # 4. Guardar notificación
        # 5. Retornar resultado
```

---

### 🟠 3. Infrastructure (Capa de Infraestructura)

**Responsabilidad**: Implementaciones técnicas concretas.

**Características**:
- Implementa interfaces definidas en Domain
- Contiene detalles técnicos (Peewee, Requests, SMTP)
- Puede ser reemplazada sin afectar la lógica

**Contenido**:

```
infrastructure/
├── database/
│   ├── connection.py                 # Singleton para conexión SQLite
│   └── models/
│       └── notification_model.py     # Modelo Peewee
├── repositories/
│   └── notification_repository_impl.py  # Implementación del repo
├── external_services/
│   ├── weather_api_service.py        # Cliente WeatherAPI
│   └── email_service.py              # Cliente SMTP
└── config/
    └── settings.py                   # Configuración desde .env
```

**Ejemplo - Repository Implementation**:
```python
class NotificationRepositoryImpl(NotificationRepository):
    """Implementa la interfaz usando Peewee"""
    
    def save(self, notification: Notification) -> Notification:
        model = NotificationModel.create(...)
        notification.id = model.id
        return notification
    
    def find_by_email(self, email: str) -> List[Notification]:
        models = NotificationModel.select().where(...)
        return [self._to_entity(m) for m in models]
```

---

### 🔴 4. Presentation (Capa de Presentación)

**Responsabilidad**: Interfaz con el mundo exterior (HTTP en este caso).

**Características**:
- Recibe requests HTTP
- Convierte a DTOs
- Llama a los casos de uso
- Retorna responses HTTP

**Contenido**:

```
presentation/
├── routes/
│   └── weather_routes.py             # Endpoints Flask
├── middlewares/
│   └── auth_middleware.py            # Autenticación API Key
└── schemas/
    └── swagger_schemas.py            # Documentación Swagger
```

**Ejemplo - Routes**:
```python
class WeatherRoutes:
    def __init__(
        self,
        check_weather_use_case: CheckWeatherUseCase,
        get_notifications_use_case: GetNotificationsUseCase
    ):
        self.check_weather_use_case = check_weather_use_case
        # ...
    
    @require_api_key
    def check_weather(self):
        data = request.get_json()
        dto = WeatherRequestDTO(...)
        result = self.check_weather_use_case.execute(dto)
        return jsonify(result)
```

---

## Flujo de Datos

### Ejemplo: POST /check_weather

```
1. [HTTP Request]
   ↓
2. [Presentation Layer]
   - WeatherRoutes.check_weather()
   - Middleware valida API Key
   - Crea WeatherRequestDTO
   ↓
3. [Application Layer]
   - CheckWeatherUseCase.execute()
   - Valida DTO
   ↓
4. [Infrastructure Layer]
   - WeatherAPIService.get_forecast()
   - Obtiene datos de API externa
   ↓
5. [Domain Layer]
   - Forecast entity
   - Lógica: requires_alert()
   ↓
6. [Application Layer]
   - Si requiere alerta:
     - EmailService.send_email()
     - NotificationRepository.save()
   ↓
7. [Presentation Layer]
   - Retorna JSON response
   ↓
8. [HTTP Response]
```

---

## Patrones Implementados

### 1. Repository Pattern

**Problema**: Necesitamos abstraer la persistencia de datos.

**Solución**: Interfaz en Domain, implementación en Infrastructure.

```python
# Domain
class NotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        pass

# Infrastructure
class NotificationRepositoryImpl(NotificationRepository):
    def save(self, notification: Notification) -> Notification:
        # Implementación con Peewee
```

### 2. Dependency Injection

**Problema**: Componentes acoplados y difíciles de testear.

**Solución**: Inyectar dependencias en el constructor.

```python
# app.py
notification_repository = NotificationRepositoryImpl()
weather_service = WeatherAPIService(...)
email_service = EmailService(...)

use_case = CheckWeatherUseCase(
    notification_repository=notification_repository,
    weather_service=weather_service,
    email_service=email_service
)
```

### 3. DTO (Data Transfer Object)

**Problema**: No queremos exponer entidades del dominio directamente.

**Solución**: Objetos específicos para transferir datos entre capas.

```python
@dataclass
class WeatherRequestDTO:
    latitude: float
    longitude: float
    email: str
    
    def validate(self) -> tuple[bool, str]:
        # Validación
```

### 4. Factory Pattern

**Problema**: Creación compleja de la aplicación.

**Solución**: Función factory que crea y configura todo.

```python
def create_app() -> Flask:
    # Cargar config
    # Crear instancias
    # Inyectar dependencias
    # Registrar blueprints
    return app
```

### 5. Singleton

**Problema**: Múltiples conexiones a la base de datos.

**Solución**: DatabaseConnection como singleton.

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls, db_name: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._db = SqliteDatabase(db_name)
        return cls._instance
```

---

## Decisiones de Diseño

### ¿Por qué separar Models de Entities?

- **Models** (Infrastructure): Representación técnica (Peewee)
- **Entities** (Domain): Representación de negocio

Esto permite cambiar de ORM sin tocar la lógica de negocio.

### ¿Por qué DTOs?

Los DTOs proveen:
- Validación de entrada
- Desacoplamiento de la API de las entidades
- Documentación clara de qué datos se necesitan

### ¿Por qué interfaces en Python?

Aunque Python es dinámico, las interfaces (ABC) proveen:
- Contrato claro
- Documentación
- Type hints para IDEs
- Base para testing con mocks

### ¿Por qué casos de uso?

Los casos de uso:
- Encapsulan la lógica de aplicación
- Son reutilizables
- Fáciles de testear
- Documentan las funcionalidades

---

## Testing

### Testear Use Cases

```python
def test_execute_with_adverse_weather():
    # Arrange
    mock_repo = Mock()
    mock_weather = Mock()
    mock_email = Mock()
    
    use_case = CheckWeatherUseCase(mock_repo, mock_weather, mock_email)
    
    # Act
    result = use_case.execute(request)
    
    # Assert
    assert result['alert_sent'] is True
    mock_email.send_email.assert_called_once()
```

---

## Beneficios Comprobados

| Aspecto | Antes | Después |
|---------|-------|---------|
| Testear lógica de negocio | Difícil (requiere DB y API) | Fácil (solo mocks) |
| Cambiar de SQLite a PostgreSQL | Tocar múltiples archivos | Solo Infrastructure |
| Cambiar de WeatherAPI a otra | Código disperso | Solo un archivo |
| Agregar nuevo canal (SMS) | Modificar lógica existente | Agregar nuevo servicio |
| Entender el código | Buscar en todos lados | Estructura clara |

---

## Conclusión

Clean Architecture no es solo "organizar carpetas", es una forma de pensar que:

- Protege la lógica de negocio
- Facilita el cambio
- Mejora la testabilidad
- Promueve la reutilización
- Hace el código más mantenible

**Inversión inicial**: Mayor (más archivos, más estructura)  
**Retorno**: Proyecto escalable, mantenible y profesional

---

**Autor**: Milton Jaramillo  
**Proyecto**: Weather Alert Service - Clean Architecture  
**Reto**: MELI Technical Challenge
