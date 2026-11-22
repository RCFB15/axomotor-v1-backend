# AxoMotor API rest - Schemas

**Entorno:** Backend

**Objetivo:** Describir los diferentes tipos de datos utilizados por la API del Sistema de Monitoreo de Vehículos en Tiempo Real.

## Cómo consultar esta información

En este documento se describe la estructura de los tipos de datos (schemas) utilizados para devolver datos al realizar una petición a un endpoint.

**Columnas:**
- Campo: Nombre del atributo usando `snake_case`.
- Tipo/Valores: Define el tipo utilizado para el campo.
- Longitud/Rango: Establece la longitud o rangos para cadenas y números.
- Incluir: Indica si el campo es requerido u opcional.

Referencias de emojis:

| Emoji | Descripción                                    |
| ----- | ---------------------------------------------- |
| 🔑    | Identificador autogenerado.                    |
| 🟢    | El valor/objeto siempre se incluye.            |
| 🟡    | El valor es opcional.                          |
| 🟣    | El objeto siempre se incluye en vista detalles.   |
| 🔵    | El objeto es opcional pero solo se incluye en vista detalles.    |

---
## Contenido

- [Token](#token)
- [User](#user)
- [UserAlert](#useralert)
- [Driver](#driver)
- [Vehicle](#vehicle)
- [VehicleService](#vehicleservice)
- [VehicleEventCode](#vehicleeventcode)
- [VehicleEvent](#vehicleevent)
- [VehicleDevice](#vehicledevice)
- [KnownLocation](#knownlocation)
- [KnownLocationSimple](#knownlocationsimple)
- [Trip](#trip)
- [Position](#position)
- [IncidentCode](#incidentcode)
- [Incident](#incident)
- [IncidentMedia](#incidentmedia)

---

## Tipos de datos

### Token

Contiene el token de acceso correspondiente a una sesión activa de un usuario.

| Campo        | Tipo   | Longitud | Incluir | Descripción                         |
| ------------ | ------ | -------- | ---- |------------------------------------ |
| access_token | String |          | 🔑   | Cadena de token de acceso.          |
| first_name   | String |          | 🟢   | Tipo de token. Siempre es `bearer`. |

### User

Representa a un usuario registrado en la plataforma AxoMotor.

| Campo           | Tipo/Valores         | Longitud | Incluir | Descripción                                                                                     |
| --------------- | -------------------- | -------- | ---- | ----------------------------------------------------------------------------------------------- |
| user_id         | UUID                 |          | 🔑   | Identificador del usuario.                                                                      |
| first_name      | String               | 2-60     | 🟢    | Nombre de pila del usuario.                                                                     |
| last_name       | String               | 2-60     | 🟡    | Apellidos del usuario.                                                                          |
| email           | String               | 120      | 🟢    | Correo electrónico del usuario.                                                                 |
| username        | String               | 3-16     | 🟢    | Nombre de usuario.                                                                              |
| phone_number    | String               | 16       | 🟢    | Número de teléfono del usuario. Se almacena en formato +XX XXX-XXX-XXXX.                        |
| password         | String              | 8-120    | 🟢    | Contraseña.                                                                            |
| role            | ADMIN, DRIVER, AGENT |          | 🟢    | Rol del usuario. Puede ser alguna de las siguiente opciones: administrador, agente o conductor. |
| is_enabled      | Boolean              |          | 🟢    | Indica si el usuario se encuentra habilitado en el sistema. Por defecto es TRUE.                |
| registered_at   | DateTime             |          | 🟢    | Marca de tiempo de registro del usuario.                                                        |
| updated_at      | DateTime             |          | 🟡    | Marca de tiempo de actualización del usuario.                                                   |
| logged_in_at    | DateTime             |          | 🟡    | Marca de tiempo de último inicio de sesión del usuario.                                         |

### UserAlert

Representa una alerta para informar de un suceso a un usuario.

| Campo      | Tipo/Valores                                                      | Longitud | Incluir | Descripción                                                                                |
| ---------- | ----------------------------------------------------------------- | -------- | ---- | ------------------------------------------------------------------------------------------ |
| alert_id   | UUID                                                              |          | 🔑   | Identificador único de la alerta.                                                          |
| user_id    | UUID                                                              |          | 🟢    | Identificador del usuario asociado a la alerta.                                            |
| title      | String                                                            | 80       | 🟢    | Título de la alerta.                                                                       |
| content    | String                                                            | 240      | 🟢    | Contenido de la alerta.                                                                    |
| type       | ACCOUNT, SYSTEM, VEHICLE_INCIDENT, TRIP_INCIDENT, INCIDENT_UPDATE |          | 🟢    | Tipo de alerta. Puede ser: cuenta, sistema, incidente en viaje, actualización de incidente |
| is_read    | Boolean                                                           |          | 🟢    | Indicador de lectura de la alerta.                                                         |
| created_at | DateTime                                                          |          | 🟢    | Marca de tiempo de creación de la alerta.                                                  |

### Driver

Representa a un conductor de vehículos registrado.

| Campo            | Tipo/Valores          | Longitud | Incluir | Descripción                                                                                                                                             |
| ---------------- | --------------------- | -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| driver_id        | UUID                  |          | 🔑   | Identificador único del conductor.                                                                                                                      |
| user_id          | UUID                  |          | 🟢    | Identificador del usuario asociado al perfil de conductor.                                                                                              |
| user             | [User](#user)         |          | 🟣    | Objeto de usuario asociado al perfil de conductor.                                      |
| telegram_user_id | Long                |          | 🟡    | Identificador del usuario asociado a la cuenta en Telegram. Se establece cuando un usuario inicia sesión a través del bot manejado por el agente de IA. |
| license_number   | String                | 8-20     | 🟢    | Número oficial de la licencia de conducir.                                                                                                              |
| license_class    | A, A1, A2, B, C, D, E |          | 🟢    | Clase de la licencia de conducir. Puede ser: A, A1, A2, B, C, D, E.                                                                                     |
| license_iss_date | Date                  |          | 🟢    | Fecha de expedición o emisión de la licencia de conducir.                                                                                               |
| license_exp_date | Date                  |          | 🟢    | Fecha de vencimiento o expiración de la licencia de conducir.                                                                                           |
| is_active        | Boolean               |          | 🟢    | Indica si el conductor se encuentra activo en el sistema.                                                                                               |
| is_enabled       | Boolean               |          | 🟢    | Indica si el conductor se encuentra habilitado para conducir.                                                                                           |
| registered_at    | DateTime              |          | 🟢    | Marca de tiempo de registro del conductor.                                                                                                              |
| updated_at       | DateTime              |          | 🟡    | Marca de tiempo de actualización del conductor.                                                                                                         |

### Vehicle

Representa a un vehículo registrado

| Campo         | Tipo                                                                                         | Longitud | Incluir | Descripción                                                                                                                                           |
| ------------- | -------------------------------------------------------------------------------------------- | -------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| vehicle_id    | UUID                                                                                         |          | 🔑   | Identificador de vehículo.                                                                                                                            |
| plate_number  | String                                                                                       | 8-12     | 🟢    | Número de placas del vehículo.                                                                                                                        |
| reg_number    | String                                                                                       | 16-22    | 🟢    | Número de registro de tarjeta de circulación del vehículo.                                                                                            |
| series_vin    | String                                                                                       | 17       | 🟢    | Número de serie del vehículo (VIN).                                                                                                                   |
| brand         | String                                                                                       | 1-60     | 🟢    | Marca del vehículo.                                                                                                                                   |
| model         | String                                                                                       | 1-60     | 🟢    | Modelo del vehículo.                                                                                                                                  |
| year          | Int                                                                                          |          | 🟢    | Año del vehículo.                                                                                                                                     |
| type          | PASSENGER_CAR, PICKUP, PANEL, VAN, BUS, TRUCK                                                |          | 🟢    | Tipo de vehículo. Puede ser: vehículo de pasajeros, camioneta, panel, van, autobus, camión.                                                           |
| status        | OPERATIVE, IN_USE, OUT_OF_SERVICE, UNDER_MAINTENANCE, DOCUMENTS_EXPIRED, HELD_BY_AUTHORITIES |          | 🟢    | Estado actual del vehículo. Puede ser: operativo, en uso, fuera de servicio, en mantenimiento, documentación expirada o retenido por las autoridades. |
| registered_at | DateTime                                                                                     |          | 🟢    | Marca de tiempo de registro del vehículo.                                                                                                             |
| updated_at    | DateTime                                                                                     |          | 🟡    | Marca de tiempo de actualización del vehículo.                                                                                                        |

### VehicleService

Representa un servicio de mantenimiento dado a un vehículo.

| Campo             | Tipo/Valores                                          | Longitud | Incluir | Descripción                                                                                                                                |
| ----------------- | ----------------------------------------------------- | -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| service_id        | UUID                                                  |          | 🔑   | Identificador de servicio.                                                                                                                 |
| vehicle_id        | UUID                                                  |          | 🟢    | Identificador del vehículo.                                                                                                                |
| status            | PENDING, IN_PROGRESS, COMPLETED, CANCELLED, DISCARDED |          | 🟢    | Estado actual del servicio de mantenimiento. Puede ser: pendiente, en progreso, completado, cancelado, descartado. Por defecto: pendiente. |
| Date              | DateTime                                              |          | 🟢    | Fecha y hora en que se realiza el servicio de mantenimiento.                                                                               |
| next_service_date | DateTime                                              |          | 🟢    | Fecha y hora estimada para el siguiente servicio de mantenimiento.                                                                         |
| created_by_id     | UUID                                                  |          | 🟢    | Identificador del usuario que crea la realización del servicio de mantenimiento.                                                           |
| created_by        | [User](#user)                                         |          | 🟣    | Objeto con información del usuario que crea la realización del servicio de mantenimiento.                                                           |
| authorized_by_id  | UUID                                                  |          | 🟡    | Identificador del usuario que autoriza la realización del servicio de mantenimiento.                                                       |
| authorized_by     | [User](#user)                                         |          | 🔵    | Objeto con información del usuario que autoriza la realización del servicio de mantenimiento.                                                       |
| registered_at     | DateTime                                              |          | 🟢    | Marca de tiempo de registro del servicio.                                                                                                  |
| updated_at        | DateTime                                              |          | 🟡    | Marca de tiempo de actualización del servicio.                                                                                             |

### VehicleEventCode

Agrega información a un evento de vehículo.

| Campo       | Tipo                    | Longitud | Incluir | Descripción                                                         |
| ----------- | ----------------------- | -------- | ---- | ------------------------------------------------------------------- |
| code        | String                  | 12       | 🔑   | Código de evento.                                                   |
| description | String                  | 40       | 🟢    | Descripción del evento.                                             |
| severity    | INFO, WARNING, CRITICAL |          | 🟢    | Severidad del evento. Puede ser: información, advertencia, crítico. |

### VehicleEvent

Representa un evento que produjo o detectó alguno de los dispositivos instalados en el vehículo.

| Campo           | Tipo/Valores           | Longitud | Requerido | Descripción                                                                            |
| --------------- | ---------------------- | -------- | --------- | -------------------------------------------------------------------------------------- |
| event_id        | UUID                   |          | 🔑        | Identificador de evento.                                                               |
| code            | String                 | 12       | 🟢         | Código identificador del tipo de evento generado por el dispositivo.                   |
| info            | [VehicleEventCode](#vehicleeventcode)                 |          | 🟢         | Objeto con información acerca del código de evento.                   |
| vehicle_id      | UUID                   |          | 🟢         | Identificador del vehículo donde está instalado el dispositivo que produjo el evento.  |
| latitude        | Decimal                |          | 🟡         | Latitud donde se originó el evento del vehículo.                      |
| longitude       | Decimal                |          | 🟡         | Longitud donde se originó el evento del vehículo.                     |
| additional_data | JSON                   |          | 🟡         | Datos complementarios o métricas en formato JSON asociados al evento.                  |
| registered_at   | DateTime               |          | 🟢         | Marca de tiempo de registro del evento.                                                |

### VehicleDevice

Representa a un dispositivo físico instalado en un vehículo.

| Campo         | Tipo      | Longitud | Incluir | Descripción                                                                                                                                                                                    |
| ------------- | --------- | -------- | ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| device_id     | UUID      |          | 🔑   | Identificador único del dispositivo telemático.                                                                                                                                                |
| vehicle_id    | UUID      |          | 🟢    | Identificador del vehículo al que está asignado e instalado el dispositivo.                                                                                                                    |
| serial_number | String    | 12       | 🟢    | Número de serie de fabricación del dispositivo.                                                                                                                                                |
| tag           | String    | 16       | 🟢    | Etiqueta o identificador alfanumérico visible asignado al dispositivo.                                                                                                                         |
| type          | HUB, NODE |          | 🟢    | Tipo de dispositivo telemático o sensor instalado en el vehículo. Puede ser: hub (concentrador que procesa los datos de los sensores), node (dispositivo equipado con sensor, cámara o ambos). |
| battery_level | Int       |          | 🟢    | Nivel porcentual o carga actual de la batería del dispositivo.                                                                                                                                 |
| is_active     | Boolean   |          | 🟢    | Indica si el dispositivo se encuentra activo y transmitiendo datos.                                                                                                                            |
| is_enabled    | Boolean   |          | 🟢    | Indica si el dispositivo se encuentra habilitado.                                                                                                                                              |
| registered_at | DateTime  |          | 🟢    | Marca de tiempo de registro del dispositivo.                                                                                                                                                   |
| updated_at    | DateTime  |          | 🟡    | Marca de tiempo de actualización del dispositivo.                                                                                                                                              |

### KnownLocation

Representa una ubicación conocida que puede utilizarse como punto de origen o destino de un viaje.

| Campo         | Tipo                    | Longitud | Incluir | Descripción                                         |
| ------------- | ----------------------- | -------- | ---- | --------------------------------------------------- |
| location_id   | UUID                    |          | 🔑   | Identificador de la ubicación.                      |
| name          | String                  | 1-60     | 🟢    | Nombre de la ubicación.                             |
| type          | String                  | 40       | 🟢    | Tipo de la ubicación.                               |
| address       | String                  | 240      | 🟢    | Dirección completa de la ubicación.                 |
| location_area | GEOMETRY(Polygon, 4326) |          | 🟢    | Polígono de la ubicación para usarla con Geocercas. |
| registered_at | DateTime                |          | 🟢    | Fecha de registro de la ubicación.                  |

### KnownLocationSimple

Representa un resumen de una ubicación conocida que puede utilizarse como punto de origen o destino de un viaje.

| Campo         | Tipo                    | Longitud | Incluir | Descripción                                         |
| ------------- | ----------------------- | -------- | ---- | --------------------------------------------------- |
| name          | String                  | 1-60     | 🟢    | Nombre de la ubicación.                             |
| type          | String                  | 40       | 🟢    | Tipo de la ubicación.                               |
| address       | String                  | 240      | 🟢    | Dirección completa de la ubicación.                 |

### Trip

Describe la información de un viaje.

| Campo          | Tipo/Valores                                                                                | Longitud | Incluir | Descripción                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------- | -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| trip_id        | UUID                                                                                        |          | 🔑   | Identificador único del viaje registrado.                                                                                                              |
| vehicle_id     | UUID                                                                                        |          | 🟢    | Identificador del vehículo asignado para realizar el viaje.                                                                                            |
| vehicle       | [Vehicle](#vehicle)                                                                                        |          | 🟣    | Objeto con información del vehículo asignado para realizar el viaje.                                                                                            |
| driver_id      | UUID                                                                                        |          | 🟢    | Identificador del conductor asignado para operar el viaje.                                                                                             |
| driver         | [Driver](#driver)                                                                                        |          | 🟣    | Objeto con información del conductor asignado para operar el viaje.                                                                                             |
| origin_id      | UUID                                                                                        |          | 🟢    | Identificador del lugar conocido configurado como punto de origen.                                                                                     |
| origin         | [KnownLocationSimple](#knownlocationsimple)                                                                                        |          | 🟣    | Objeto con información del lugar conocido configurado como punto de origen.                                                                                     |
| destination_id | UUID                                                                                        |          | 🟢    | Identificador del lugar conocido configurado como punto de destino.                                                                                    |
| destination | [KnownLocationSimple](#knownlocationsimple)                                                                                        |          | 🟣    | Objeto con información del lugar conocido configurado como punto de destino.                                                                                    |
| departure_date | DateTime                                                                                    |          | 🟢    | Fecha y hora programada o estimada de salida del viaje.                                                                                                |
| arrive_date    | DateTime                                                                                    |          | 🟢    | Fecha y hora programada o estimada de llegada al destino.                                                                                              |
| status         | PLANNED, DELAYED, ON_ROUTE, AT_BASE, STOPPED, FINISHED, CANCELLED, ABORTED, GPS_SIGNAL_LOST |          | 🟢    | Estado actual del viaje en el sistema. Puede ser: planeado, retrasado, en ruta, en base, detenido, finalizado, cancelado, abortado, señal GPS perdida. |
| distance       | Decimal                                                                                     | 5,2      | 🟡    | Distancia total recorrida durante el trayecto del viaje en kilómetros.                                                                                 |
| average_speed  | Decimal                                                                                     | 5,2      | 🟡    | Velocidad promedio registrada durante el viaje en km/h.                                                                                                |
| created_at     | DateTime                                                                                    |          | 🟢    | Marca de tiempo de la creación del viaje.                                                                                                              |
| started_at     | DateTime                                                                                    |          | 🟡    | Marca de tiempo real de inicio del viaje.                                                                                                              |
| finished_at    | DateTime                                                                                    |          | 🟡    | Marca de tiempo real de finalización o cierre del viaje.                                                                                               |

### Position

Describe la posición GPS de un vehículo en un momento dado.

| Campo         | Tipo                   | Longitud | Incluir | Descripción                                                          |
| ------------- | ---------------------- | -------- | ---- | -------------------------------------------------------------------- |
| position_id   | UUID                   |          | 🔑   | Identificador único del registro de posición.                        |
| vehicle_id    | UUID                   |          | 🟢    | Identificador del vehículo que registro la posición. |
| trip_id       | UUID                   |          | 🟡    | Identificador del viaje al cual corresponde el registro de posición. |
| latitude      | Decimal                |          | 🟢    | Latitud registrada del vehículo en el trayecto.                      |
| longitude     | Decimal                |          | 🟢    | Longitud registrada del vehículo en el trayecto.                     |
| speed         | Decimal                | 5,2      | 🟢    | Velocidad instantánea registrada del vehículo en km/h.               |
| registered_at | DateTime               |          | 🟢    | Marca de tiempo de captura de la posición.                           |

### IncidentCode

Establece la información acerca de una incidencia.

| Campo       | Tipo                    | Longitud | Incluir | Descripción                                                               |
| ----------- | ----------------------- | -------- | ---- | ------------------------------------------------------------------------- |
| code        | String                  | 12       | 🔑   | Código de la incidencia.                                                  |
| description | String                  | 40       | 🟢    | Descripción de la incidencia.                                             |
| severity    | INFO, WARNING, CRITICAL |          | 🟢    | Severidad de la incidencia. Puede ser: información, advertencia, crítico. |

### Incident

Describe la información acerca de un incidente producido durante un viaje.

| Campo               | Tipo/Valores                         | Longitud | Incluir | Descripción                                                                                                                          |
| ------------------- | ------------------------------------ | -------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------ |
| incident_id         | UUID                                 |          | 🔑   | Identificador único de la incidencia reportada.                                                                                      |
| trip_id             | UUID                                 |          | 🟢    | Identificador del viaje durante el cual ocurrió la incidencia.                                                                       |
| trip                | [Trip](#trip)                        |          | 🟣    | Objeto con información del viaje durante el cual ocurrió la incidencia.                                                                       |
| code                | String                               | 12       | 🟢    | Código de referencia del tipo de incidencia.                                                                            |
| info                | [IncidentCode](#incidentcode)        |          | 🟢    | Objeto con información acerca del tipo de incidencia.                                                                            |
| status              | OPEN, IN_REVISION, CLOSED, DISCARDED |          | 🟢    | Estado actual de atención o resolución de la incidencia. Puede ser: abierto, en revisión, cerrado, descartado. Por defecto: abierto. |
| latitude            | Decimal                              |          | 🟡    | Latitud donde ocurrió la incidencia.                      |
| longitude           | Decimal                              |          | 🟡    | Longitud donde ocurrió la incidencia.                     |
| description         | String                             | 2-500    | 🟢    | Descripción detallada de los hechos ocurridos en la incidencia.                                                                      |
| comments            | String                             | 2-500    | 🟡    | Comentarios u observaciones de seguimiento por parte del agente.                                                                     |
| related_incident_id | UUID                                 |          | 🟡    | Identificador de la incidencia vinculada o relacionada para dar seguimiento.                                                         |
| registered_at       | DateTime                             |          | 🟢    | Marca de tiempo de registro de la incidencia.                                                                                        |
| reviewed_at         | DateTime                             |          | 🟡    | Marca de tiempo en que la incidencia fue revisada por el agente.                                                                     |
| closed_at           | DateTime                             |          | 🟡    | Marca de tiempo en que la incidencia fue cerrada o resuelta.                                                                         |
| created_by_id       | UUID                                 |          | 🟢    | Identificador del usuario que registró la incidencia.                                                                                |
| created_by          | [User](#user)                        |          | 🔵    | Objeto con información del usuario que registró la incidencia.                                                                                |
| reviewed_by_id      | UUID                                 |          | 🟡    | Identificador del agente asignado para atender la incidencia.                                                                        |
| reviewed_by         | [User](#user)                        |          | 🔵    | Objeto con información del agente asignado para atender la incidencia.                                                                        |

### IncidentMedia

Representa un archivo multimedia captado antes o durante una incidencia en un viaje.

| Campo         | Tipo/Valores | Longitud | Requerido | Descripción                                                               |
| ------------- | ------------ | -------- | --------- | ------------------------------------------------------------------------- |
| media_id      | UUID         |          | 🔑        | Identificador único de la evidencia multimedia.                           |
| incident_id   | UUID         |          | 🟢         | Identificador de la incidencia vinculada al archivo multimedia.           |
| file_url      | String       |          | 🟢         | Identificador o ruta del archivo en el repositorio de almacenamiento.     |
| type          | IMAGE, VIDEO |          | 🟢         | Tipo de evidencia multimedia capturada. Puede ser de tipo imagen o vídeo. |
| file_metadata | JSON         |          | 🟢         | Metadatos del archivo de evidencia multimedia.                            |
| captured_at   | DateTime     |          | 🟢         | Marca de tiempo en la que fue capturada la evidencia multimedia.          |
| uploaded_at   | DateTime     |          | 🟢         | Marca de tiempo en la que se completó la subida del archivo al servidor.  |
