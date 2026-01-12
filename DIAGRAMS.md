# Diagrama de Clean Architecture - Weather Alert Service

## Vista General de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│                     (Flask Routes & HTTP)                        │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ WeatherRoutes  │  │ Auth         │  │ Swagger Schemas  │   │
│  │                │  │ Middleware   │  │                  │   │
│  └────────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                          │
│                    (Use Cases & Business Logic)                  │
│  ┌──────────────────────┐  ┌────────────────────────────┐      │
│  │ CheckWeatherUseCase  │  │ GetNotificationsUseCase    │      │
│  │                      │  │                            │      │
│  └──────────────────────┘  └────────────────────────────┘      │
│                                                                  │
│  ┌────────────────────┐  ┌──────────────────────┐              │
│  │ WeatherRequestDTO  │  │ NotificationDTO      │              │
│  └────────────────────┘  └──────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         DOMAIN LAYER                             │
│                  (Entities & Repository Interfaces)              │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │   Forecast   │  │ Notification │   (Entities)                │
│  └──────────────┘  └──────────────┘                            │
│                                                                  │
│  ┌────────────────────────────────────────┐                     │
│  │  NotificationRepository (Interface)    │                     │
│  │  - save()                              │                     │
│  │  - find_by_email()                     │                     │
│  └────────────────────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                         │
│              (Technical Implementations & External Services)     │
│                                                                  │
│  DATABASE                  REPOSITORIES                          │
│  ┌──────────────────┐    ┌────────────────────────────┐        │
│  │ DatabaseConn     │    │ NotificationRepositoryImpl │        │
│  │ (SQLite)         │    │ (implements interface)     │        │
│  └──────────────────┘    └────────────────────────────┘        │
│  ┌──────────────────┐                                           │
│  │ NotificationModel│                                           │
│  │ (Peewee ORM)     │                                           │
│  └──────────────────┘                                           │
│                                                                  │
│  EXTERNAL SERVICES         CONFIGURATION                         │
│  ┌──────────────────┐    ┌──────────────┐                      │
│  │ WeatherAPIService│    │   Settings   │                      │
│  │ (HTTP Client)    │    │   (.env)     │                      │
│  └──────────────────┘    └──────────────┘                      │
│  ┌──────────────────┐                                           │
│  │   EmailService   │                                           │
│  │   (SMTP)         │                                           │
│  └──────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Ejecución: POST /check_weather

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ HTTP POST /check_weather
     │ Headers: x-api-key
     │ Body: {lat, lon, email}
     ↓
┌────────────────────────┐
│  AuthMiddleware        │ ← Valida API Key
│  @require_api_key      │
└────────┬───────────────┘
         │ ✓ Authorized
         ↓
┌────────────────────────┐
│  WeatherRoutes         │
│  check_weather()       │ ← Recibe request
└────────┬───────────────┘
         │ 1. Parse JSON
         │ 2. Create DTO
         ↓
┌─────────────────────────────────┐
│  CheckWeatherUseCase            │
│  execute(WeatherRequestDTO)     │ ← Orquesta lógica
└────────┬────────────────────────┘
         │
         │ 3. Validate DTO
         ↓
┌────────────────────────┐
│  WeatherAPIService     │
│  get_forecast()        │ ← Consulta API externa
└────────┬───────────────┘
         │ 4. HTTP Request
         │    to WeatherAPI.com
         ↓
┌────────────────────────┐
│  Forecast Entity       │
│  (Domain)              │ ← Crea entidad
└────────┬───────────────┘
         │ 5. Business Rule:
         │    requires_alert()?
         ↓
         ├─── SI (Adverse Weather)
         │    │
         │    ↓
         │    ┌────────────────────────┐
         │    │  EmailService          │
         │    │  send_email()          │ ← Envía alerta
         │    └────────────────────────┘
         │    │ 6. SMTP
         │    ↓
         │    ┌────────────────────────────────┐
         │    │  NotificationRepositoryImpl    │
         │    │  save()                        │ ← Guarda en DB
         │    └────────┬───────────────────────┘
         │             │ 7. Peewee ORM
         │             ↓
         │    ┌────────────────────────┐
         │    │  NotificationModel     │
         │    │  (SQLite)              │
         │    └────────────────────────┘
         │
         └─── NO (Normal Weather)
              │
              ↓
┌────────────────────────┐
│  Result Dict           │
│  {                     │
│    forecast: "...",    │
│    alert_sent: bool,   │
│    message: "..."      │
│  }                     │
└────────┬───────────────┘
         │ 8. Return to route
         ↓
┌────────────────────────┐
│  WeatherRoutes         │
│  jsonify(result)       │ ← Serializa respuesta
└────────┬───────────────┘
         │ 9. HTTP Response
         ↓
┌──────────┐
│  Client  │ ← Recibe JSON
└──────────┘
```

## Dependencias entre Capas

```
          ┌─────────────────────────────────┐
          │     DOMAIN (Core)               │
          │  - Entities                     │
          │  - Repository Interfaces        │
          │  - Business Rules               │
          │  (NO dependencies)              │
          └────────────▲────────────────────┘
                       │
                       │ implements
                       │ & depends on
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
    │                  │                  │
┌───▼─────────┐  ┌────▼─────────┐  ┌────▼──────────┐
│APPLICATION  │  │INFRASTRUCTURE│  │ PRESENTATION  │
│- Use Cases  │  │- Repos Impl  │  │ - Routes      │
│- DTOs       │  │- DB Models   │  │ - Middlewares │
│             │  │- Ext Services│  │ - Schemas     │
│             │  │- Config      │  │               │
└─────────────┘  └──────────────┘  └───────────────┘
                       │
                       │ uses
                       │
                       ↓
              ┌────────────────┐
              │ External World │
              │ - Database     │
              │ - APIs         │
              │ - SMTP         │
              └────────────────┘
```

## Inyección de Dependencias (app.py)

```
┌──────────────────────────────────────────────────────────┐
│                        app.py                            │
│                   (Composition Root)                     │
│                                                          │
│  1. Load Environment Variables (.env)                   │
│     ↓                                                    │
│  2. Create Infrastructure Instances:                    │
│     ├─ NotificationRepositoryImpl                       │
│     ├─ WeatherAPIService(api_key, url)                  │
│     └─ EmailService(smtp_server, username, password)    │
│     ↓                                                    │
│  3. Inject into Application Layer (Use Cases):          │
│     ├─ CheckWeatherUseCase(                             │
│     │     repository,                                   │
│     │     weather_service,                              │
│     │     email_service                                 │
│     │  )                                                │
│     └─ GetNotificationsUseCase(repository)              │
│     ↓                                                    │
│  4. Inject into Presentation Layer (Routes):            │
│     └─ WeatherRoutes(                                   │
│           check_weather_use_case,                       │
│           get_notifications_use_case                    │
│        )                                                │
│     ↓                                                    │
│  5. Register Blueprint in Flask App                     │
│     app.register_blueprint(routes.get_blueprint())      │
│                                                          │
│  6. Run Flask Server                                    │
│     app.run()                                           │
└──────────────────────────────────────────────────────────┘
```

## Testing con Mocks

```
Test: CheckWeatherUseCase

┌────────────────────────┐
│   TEST                 │
└────────┬───────────────┘
         │
         │ 1. Create Mocks
         ↓
┌────────────────────────┐
│  Mock Repository       │ ← No real database
└────────────────────────┘
┌────────────────────────┐
│  Mock WeatherService   │ ← No real API calls
└────────────────────────┘
┌────────────────────────┐
│  Mock EmailService     │ ← No real emails
└────────────────────────┘
         │
         │ 2. Inject Mocks
         ↓
┌────────────────────────────┐
│  CheckWeatherUseCase       │
│  (with injected mocks)     │ ← Unit under test
└────────┬───────────────────┘
         │
         │ 3. Execute
         │    use_case.execute(dto)
         ↓
┌────────────────────────┐
│  Assertions            │
│  - assert result       │
│  - mock.assert_called  │
└────────────────────────┘
```

## Beneficios Visualizados

```
CAMBIO: Migrar de SQLite a PostgreSQL

❌ Sin Clean Architecture:
   ┌──────────────────────────────────────┐
   │ Cambios en múltiples archivos:      │
   │ - routes.py                          │
   │ - services.py                        │
   │ - models.py                          │
   │ - utils.py                           │
   │ - tests (muchos)                     │
   └──────────────────────────────────────┘

✅ Con Clean Architecture:
   ┌──────────────────────────────────────┐
   │ Cambios solo en Infrastructure:      │
   │ - database/connection.py             │
   │ - database/models/                   │
   │                                      │
   │ Domain, Application, Presentation    │
   │ NO CAMBIAN                           │
   └──────────────────────────────────────┘
```

---

**Conclusión**: Clean Architecture nos da una estructura visual clara donde cada componente tiene su lugar y propósito definido.
