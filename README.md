# 🌦️ Weather Alert Service - Clean Architecture

Este proyecto es un servicio REST desarrollado con Flask que consulta el pronóstico del clima para una ubicación específica y envía alertas por correo electrónico si se detectan condiciones meteorológicas adversas.

**Refactorizado con Clean Architecture** para mejorar la mantenibilidad, escalabilidad y testabilidad del código.

---

## 🏗️ Arquitectura Clean (Clean Architecture)

Este proyecto sigue los principios de **Clean Architecture**, separando el código en capas con responsabilidades bien definidas:

```
weather-alert-clean/
├── domain/                          # Capa de Dominio
│   ├── entities/                    # Entidades del negocio
│   │   ├── forecast.py              # Entidad Pronóstico
│   │   └── notification.py          # Entidad Notificación
│   └── repositories/                # Interfaces de repositorios
│       └── notification_repository.py
│
├── application/                     # Capa de Aplicación
│   ├── use_cases/                   # Casos de uso (lógica de negocio)
│   │   ├── check_weather_use_case.py
│   │   └── get_notifications_use_case.py
│   └── dto/                         # Data Transfer Objects
│       ├── weather_request_dto.py
│       └── notification_dto.py
│
├── infrastructure/                  # Capa de Infraestructura
│   ├── database/                    # Base de datos
│   │   ├── connection.py            # Conexión a SQLite
│   │   └── models/                  # Modelos ORM
│   │       └── notification_model.py
│   ├── repositories/                # Implementaciones de repositorios
│   │   └── notification_repository_impl.py
│   ├── external_services/           # Servicios externos
│   │   ├── weather_api_service.py   # Integración con WeatherAPI
│   │   └── email_service.py         # Servicio de email SMTP
│   └── config/                      # Configuración
│       └── settings.py
│
├── presentation/                    # Capa de Presentación
│   ├── routes/                      # Rutas HTTP
│   │   └── weather_routes.py
│   ├── middlewares/                 # Middlewares
│   │   └── auth_middleware.py
│   └── schemas/                     # Esquemas Swagger
│       └── swagger_schemas.py
│
├── tests/                           # Tests unitarios
│   ├── test_weather_use_case.py
│   └── test_notification_use_case.py
│
├── app.py                           # Punto de entrada (Dependency Injection)
├── requirements.txt
├── .env
└── README.md
```

---

## 🎯 Principios de Clean Architecture Aplicados

### 1. **Separación de Responsabilidades**
Cada capa tiene una responsabilidad única:
- **Domain**: Reglas de negocio puras (sin dependencias externas)
- **Application**: Casos de uso y flujos de aplicación
- **Infrastructure**: Implementaciones técnicas (DB, APIs, Email)
- **Presentation**: Interfaz HTTP con Flask

### 2. **Inversión de Dependencias**
Las capas internas no dependen de las externas. La capa de dominio define interfaces (ej: `NotificationRepository`) que son implementadas por la capa de infraestructura.

### 3. **Inyección de Dependencias**
Todas las dependencias se inyectan en el archivo `app.py`, facilitando el testing y el mantenimiento.

### 4. **Testabilidad**
Cada componente puede ser testeado de forma aislada usando mocks.

---

## ✨ Características

- ✅ Consulta la API de [WeatherAPI](https://www.weatherapi.com/)
- ✅ Detecta condiciones climáticas adversas (tormentas, nieve, niebla, etc.)
- ✅ Envía notificaciones por correo electrónico
- ✅ Registra notificaciones en SQLite
- ✅ Autenticación con API Key
- ✅ Documentación Swagger interactiva
- ✅ Tests unitarios con Pytest
- ✅ **Clean Architecture**
- ✅ **Inyección de dependencias**
- ✅ **Alta mantenibilidad y escalabilidad**

---

## 🛠️ Tecnologías

- **Python 3.10+**
- **Flask** (Framework web)
- **Peewee** (ORM)
- **Flasgger** (Documentación Swagger)
- **Pytest** (Testing)
- **Requests** (HTTP client)
- **SMTP** (Envío de emails)

---

## ⚙️ Configuración

### Variables de entorno (`.env`)

```env
# Seguridad
API_KEY=milton_1234

# WeatherAPI
WEATHER_API_KEY=tu_api_key_aqui
WEATHER_API_URL=http://api.weatherapi.com/v1/forecast.json
WEATHER_DAYS=2

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_password_de_aplicacion
MAIL_USE_TLS=True

# Database
DATABASE_NAME=weather_alerts.db
```

---

## 🚀 Instrucciones de Uso

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` con las variables mencionadas arriba.

### 3. Ejecutar tests

```bash
pytest tests -v
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

---

## 📚 Documentación API (Swagger)

Una vez ejecutada la aplicación, puedes acceder a la documentación interactiva:

**Local**: http://localhost:5000/apidocs/

**Producción (Render)**: https://weatherapi-x181.onrender.com/apidocs/

**API Key para pruebas**: `milton_1234`

---

## 🧪 Endpoints

### 1. POST `/check_weather`
Verifica el clima y envía alertas si es necesario.

**Headers:**
```
x-api-key: milton_1234
```

**Body:**
```json
{
  "latitude": 5.07,
  "longitude": -75.52,
  "email": "correo@ejemplo.com"
}
```

### 2. GET `/notifications?email=correo@ejemplo.com`
Obtiene el historial de notificaciones enviadas.

**Headers:**
```
x-api-key: milton_1234
```

---

## 🧩 Ventajas de Clean Architecture

### ✅ Alta Mantenibilidad
- Cambios en la base de datos no afectan la lógica de negocio
- Fácil reemplazar servicios externos (ej: cambiar de WeatherAPI a otra API)
- Código organizado y fácil de entender

### ✅ Escalabilidad
- Agregar nuevos tipos de alertas (contaminación, sismos, etc.)
- Integrar nuevos canales de notificación (SMS, Push, Slack, etc.)
- Sin afectar el código existente

### ✅ Testabilidad
- Cada capa se puede testear de forma aislada
- Uso de mocks para simular dependencias
- Tests rápidos y confiables

### ✅ Reutilización
- Los casos de uso pueden ser reutilizados en diferentes interfaces (CLI, API, WebSockets)
- La lógica de negocio es independiente del framework

---

## 🔄 Flujo de Ejecución

1. **Usuario** hace una petición HTTP → `presentation/routes/weather_routes.py`
2. **Middleware** valida la API Key → `presentation/middlewares/auth_middleware.py`
3. **Controller** crea un DTO y llama al Use Case → `application/use_cases/check_weather_use_case.py`
4. **Use Case** orquesta la lógica:
   - Consulta el clima → `infrastructure/external_services/weather_api_service.py`
   - Si hay clima adverso:
     - Envía email → `infrastructure/external_services/email_service.py`
     - Guarda notificación → `infrastructure/repositories/notification_repository_impl.py`
5. **Repository** persiste en la base de datos → `infrastructure/database/models/notification_model.py`
6. **Response** se devuelve al usuario

---

## 🎓 Diferencias con la Versión Anterior

| Aspecto | Versión Anterior | Clean Architecture |
|---------|-----------------|-------------------|
| Estructura | Archivos planos | Capas bien definidas |
| Dependencias | Acoplamiento directo | Inyección de dependencias |
| Testing | Difícil de testear | Fácil con mocks |
| Mantenibilidad | Media | Alta |
| Escalabilidad | Limitada | Muy alta |
| Reutilización | Baja | Alta |

---

## 👨‍💻 Autor

**Milton Jaramillo**  
Desarrollador Full Stack  
*Este proyecto representa no solo un desafío técnico, sino también personal.*  
*¡Vamos Milton! MELI es solo el comienzo :)*

---

## 📝 Licencia

Este proyecto es parte de un reto técnico.
