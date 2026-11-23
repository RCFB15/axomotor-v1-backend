# AxoMotor API rest

**Entorno:** Backend

**Objetivo:** Acceso a la información del Sistema de Monitoreo de Vehículos en Tiempo Real

## Contenido

- [Usuarios](#usuarios)
- [Alertas de usuarios](#alertas-de-usuarios)
- [Conductores](#conductores)
- [Vehículos](#vehículos)
- [Servicios a vehículos](#servicios-a-vehículos)
- [Dispositivos en vehículos](#dispositivos-en-vehículos)
- [Ubicaciones conocidas](#ubicaciones-conocidas)
- [Viajes](#viajes)
- [Incidentes](#incidentes)
- [Catalogo de códigos](#catalogo-de-códigos)

## Endpoints

### Usuarios

| Método | URL                                       | Descripción                                           | Respuesta                               |
| ------ | ----------------------------------------- | ----------------------------------------------------- | --------------------------------------- |
| POST   | `/api/v1/users/token`                     | Inicio de sesión para obtener token de acceso.        | [Token](../schemas/readme.md#token)     |
| GET    | `/api/v1/users/me`                        | Obtiene el usuario actual que ha iniciado sesión.     | [User](../schemas/readme.md#user)       |
| GET    | `/api/v1/users`                           | Obtiene un listado de los usuarios registrados.       | List[[User](../schemas/readme.md#user)] |
| GET    | `/api/v1/users/{user_id}`                 | Obtiene los detalles de un usuario específico.        | [User](../schemas/readme.md#user)       |
| POST   | `/api/v1/users`                           | Registra un nuevo usuario.                            | [User](../schemas/readme.md#user)       |
| PUT    | `/api/v1/users/{user_id}`                 | Actualiza la información de un usuario en específico. | [User](../schemas/readme.md#user)       |
| PUT    | `/api/v1/users/{user_id}/change_password` | Actualiza la contraseña de un usuario en específico.  |                                         |

### Alertas de usuarios

| Método | URL                         | Descripción                             | Respuesta |
| ------ | --------------------------- | --------------------------------------- | --------- |
| GET    | `/api/v1/alerts`            | Obtiene las alertas del usuario actual. |           |
| PUT    | `/api/v1/alerts/{alert_id}` | Actualiza una alerta en específico.     |           |
| DELETE | `/api/v1/alerts`            | Elimina las alertas del usuario actual. |           |
| DELETE | `/api/v1/alerts/{user_id}`  | Elimina una alerta en específico.       |           |

### Conductores

| Método | URL                                 | Descripción                                                | Respuesta |
| ------ | ----------------------------------- | ---------------------------------------------------------- | --------- |
| GET    | `/api/v1/drivers`                   | Obtiene un listado de los conductores registrados.         |           |
| GET    | `/api/v1/drivers/{driver_id}`       | Obtiene los detalles de un conductor en específico.        |           |
| POST   | `/api/v1/drivers`                   | Registra un nuevo conductor.                               |           |
| PUT    | `/api/v1/drivers/{driver_id}`       | Actualiza la información de un conductor en específico.    |           |

### Vehículos

| Método | URL                                       | Descripción                                                  | Respuesta |
| ------ | ----------------------------------------- | ------------------------------------------------------------ | --------- |
| GET    | `/api/v1/vehicles`                        | Obtiene un listado de los vehículos registrados.             |           |
| GET    | `/api/v1/vehicles/{vehicle_id}`           | Obtiene los detalles de un vehículo en específico.           |           |
| POST   | `/api/v1/vehicles`                        | Registra un nuevo vehículo.                                  |           |
| PUT    | `/api/v1/vehicles/{vehicle_id}`           | Actualiza la información de un vehículo en específico.       |           |
| GET    | `/api/v1/vehicles/{vehicle_id}/positions` | Obtiene el registro de posiciones de vehículo en específico. |           |
| GET    | `/api/v1/vehicles/{vehicle_id}/events`    | Obtiene el registro de eventos de un vehículo en específico. |           |
| POST   | `/api/v1/vehicles/{vehicle_id}/events`    | Registra un evento de un vehículo.                           |           |

### Servicios a vehículos

| Método | URL                                       | Descripción                                                  | Respuesta |
| ------ | ----------------------------------------- | ------------------------------------------------------------ | --------- |
| GET    | `/api/v1/vehicle_services`                | Obtiene un listado de los servicios registrados.             |           |
| GET    | `/api/v1/vehicle_services/{service_id}`   | Obtiene los detalles de un servicio en específico.           |           |
| POST   | `/api/v1/vehicle_services`                | Registra un nuevo servicio.                                  |           |
| PUT    | `/api/v1/vehicle_services/{service_id}`   | Actualiza la información de un servicio en específico.       |           |

### Dispositivos en vehículos

| Método | URL                                     | Descripción                                                  | Respuesta |
| ------ | --------------------------------------- | ------------------------------------------------------------ | --------- |
| GET    | `/api/v1/vehicle_devices`               | Obtiene un listado de los dispositivos registrados.          |           |
| GET    | `/api/v1/vehicle_devices/{device_id}`   | Obtiene los detalles de un dispositivo en específico.        |           |
| POST   | `/api/v1/vehicle_devices`               | Registra un nuevo dispositivo.                               |           |
| PUT    | `/api/v1/vehicle_devices/{device_id}`   | Actualiza la información de un dispositivo en específico.    |           |

### Ubicaciones conocidas

| Método | URL                               | Descripción                                              | Respuesta |
| ------ | --------------------------------- | -------------------------------------------------------- | --------- |
| GET    | `/api/v1/locations`               | Obtiene un listado de las ubicaciones registrados.       |           |
| GET    | `/api/v1/locations/{location_id}` | Obtiene los detalles de una ubicación en específica.     |           |
| POST   | `/api/v1/locations`               | Registra una nueva ubicación conocida.                   |           |
| PUT    | `/api/v1/locations/{location_id}` | Actualiza la información de una ubicación en específica. |           |

### Viajes

| Método | URL                                 | Descripción                                         | Respuesta |
| ------ | ----------------------------------- | --------------------------------------------------- | --------- |
| GET    | `/api/v1/trips`                     | Obtiene un listado de los viajes registrados.       |           |
| GET    | `/api/v1/trips/{trip_id}`           | Obtiene los detalles de un viaje en específico.     |           |
| POST   | `/api/v1/trips`                     | Registra un nuevo viaje.                            |           |
| PUT    | `/api/v1/trips/{trip_id}`           | Actualiza la información de un viaje en específico. |           |
| GET    | `/api/v1/trips/{trip_id}/positions` | Obtiene las posiciones de un viaje en específico.   |           |

### Incidentes

| Método | URL                                     | Descripción                                                    | Respuesta |
| ------ | --------------------------------------- | -------------------------------------------------------------- | --------- |
| GET    | `/api/v1/incidents`                     | Obtiene un listado de los incidentes registrados.              |           |
| GET    | `/api/v1/incidents/{incident_id}`       | Obtiene los detalles de un incidente en específico.            |           |
| POST   | `/api/v1/incidents`                     | Registra un nuevo incidente.                                   |           |
| PUT    | `/api/v1/incidents/{incident_id}`       | Actualiza la información de un incidente en específico.        |           |
| GET    | `/api/v1/incidents/{incident_id}/media` | Obtiene los archivos multimedia de un incidente en específico. |           |
| POST   | `/api/v1/incidents/{incident_id}/media` | Sube un archivo multimedia de un incidente en específico.      |           |

### Catalogo de códigos

| Método | URL                                     | Descripción                        | Respuesta |
| ------ | --------------------------------------- | ---------------------------------- | --------- |
| GET    | `/api/v1/codes/incidents` | Obtiene un listado de los códigos de incidentes. |           |
| GET    | `/api/v1/codes/events`    | Obtiene un listado de los códigos de eventos.    |           |
