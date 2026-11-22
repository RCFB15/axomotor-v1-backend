# AxoMotor API rest - DB Models

**Entorno:** Backend

**Objetivo:** Describir los diferentes modelos de la base de datos del Sistema de Monitoreo de Vehículos en Tiempo Real.

## Cómo consultar esta información

En este documento se describe la estructura de los modelos de datos utilizados para almacenar la información en la base de datos principal en el backend.

**Columnas:**
- Columna: Nombre del atributo usando `snake_case`.
- Tipo: Define el tipo utilizado para el atributo.
- Longitud/Rango: Establece la longitud o rangos para cadenas y números.
- Restricción: Indica si el atributo está sujeto a determinadas condiciones como clave primaria (PK), clave foranea (FK), no nulo (NOT NULL), valor predeterminado (NULL) o condición (CHECK).

## Contenido

[users](#users)

[user_alerts](#user_alerts)

[drivers](#drivers)

[vehicles](#vehicles)

[vehicle_services](#vehicle_services)

[vehicle_event_codes](#vehicle_event_codes)

[vehicle_events](#vehicle_events)

[vehicle_devices](#vehicle_devices)

[known_locations](#known_locations)

[trips](#trips)

[positions](#positions)

[incident_codes](#incident_codes)

[incidents](#incidents)

[incident_media](#incident_media)

## Tablas

### users

Almacena la información y credenciales de usuarios en el sistema.

| Columna         | Tipo                       | Longitud | Restricción       | Descripción                                                                                    |
| --------------- | -------------------------- | -------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| user_id         | UUID                       |          | PK                | Identificador del usuario.                                                                     |
| first_name      | STRING                     | 2-60     | NOT NULL          | Nombre de pila del usuario.                                                                    |
| last_name       | STRING                     | 2-61     |                   | Apellidos del usuario.                                                                         |
| email           | STRING                     | 120      | NOT NULL, UNIQUE  | Correo electrónico del usuario.                                                                |
| username        | STRING                     | 3-16     | NOT NULL, UNIQUE  | Nombre de usuario.                                                                             |
| phone_number    | STRING                     | 16       | NOT NULL, UNIQUE  | Número de teléfono del usuario. Se almacena en formato +XX-XXX-XXX-XXXX.                       |
| hashed_password | STRING                     |          | NOT NULL          | Contraseña hasheada.                                                                           |
| role            | ENUM(ADMIN, DRIVER, AGENT) |          | NOT NULL          | Rol del usuario. Puede ser alguna de las siguiente opciones: administrador, conductor, agente. |
| is_enabled      | BOOLEAN                    |          | NOT NULL, DEFAULT | Indica si el usuario se encuentra habilitado en el sistema. Por defecto es TRUE.               |
| registered_at   | TIMESTAMP                  |          | NOT NULL, DEFAULT | Marca de tiempo de registro del usuario. Por defecto es la fecha y hora actual.                |
| updated_at      | TIMESTAMP                  |          | ON UPDATE         | Marca de tiempo de actualización del usuario. Por defecto es la fecha y hora actual.           |
| logged_in_at    | TIMESTAMP                  |          |                   | Marca de tiempo de último inicio de sesión del usuario.                                        |

### user_alerts

Almacena las alertas generadas por el sistema para notificar a los usuarios sobre eventos importantes.

| Columna    | Tipo      | Longitud | Restricción       | Descripción                                                                                            |
| ---------- | --------- | -------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| alert_id   | UUID      |          | PK                | Identificador único de la alerta.                                                                      |
| user_id    | UUID      |          | FK, NOT NULL      | Identificador del usuario asociado a la alerta. Se relaciona con la columna user_id de la tabla [users](#users). |
| title      | STRING    | 80       | NOT NULL          | Título de la alerta.                                                                                   |
| content    | STRING    | 240      |                   | Contenido de la alerta.                                                                                |
| type       | ENUM      |          | NOT NULL          | Tipo de alerta.                                                                                        |
| is_read    | BOOLEAN   |          | NOT NULL          | Indicador de lectura de la alerta.                                                                     |
| created_at | TIMESTAMP |          | NOT NULL, DEFAULT | Marca de tiempo de creación de la alerta. Por defecto es la fecha y hora actual.                       |

### drivers

Almacena la información adicional de los conductores registrados.

| Columna          | Tipo                        | Longitud | Restricción          | Descripción                                                                                                                                           |
| ---------------- | --------------------------- | -------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| driver_id        | UUID                        |          | PK                   | Identificador único del conductor.                                                                                                                    |
| user_id          | UUID                        |          | FK, NOT NULL, UNIQUE | Identificador del usuario asociado al perfil de conductor. Se relaciona con la columna user_id de la tabla [users](#users).                                     |
| telegram_user_id | BIGINT                      |          |                      | Identificador del usuario asociado a la cuenta en Telegram. Se obtiene cuando un usuario inicia sesión a través del bot manejado por el agente de IA. |
| license_number   | STRING                      |          | NOT NULL             | Número oficial de la licencia de conducir.                                                                                                            |
| license_class    | ENUM(A, A1, A2, B, C, D, E) |          | NOT NULL             | Clase de la licencia de conducir. Puede ser: A, A1, A2, B, C, D, E.                                                                                   |
| license_iss_date | DATE                        |          | NOT NULL             | Fecha de expedición o emisión de la licencia de conducir.                                                                                             |
| license_exp_date | DATE                        |          | NOT NULL             | Fecha de vencimiento o expiración de la licencia de conducir.                                                                                         |
| is_active        | BOOLEAN                     |          | NOT NULL             | Indica si el conductor se encuentra activo en el sistema.                                                                                             |
| is_enabled       | BOOLEAN                     |          | NOT NULL, DEFAULT    | Indica si el conductor se encuentra habilitado para conducir. Por defecto: TRUE.                                                                      |
| registered_at    | TIMESTAMP                   |          | NOT NULL, DEFAULT    | Marca de tiempo de registro del conductor. Por defecto es la fecha y hora actual.                                                                     |
| updated_at       | TIMESTAMP                   |          | ON UPDATE            | Marca de tiempo de actualización del conductor. Por defecto es la fecha y hora actual.                                                                |

### linking_tokens

Almacena los tokens de vinculación de los conductores con el bot de Telegram.

| Columna    | Tipo      | Longitud | Restricción       | Descripción                                                                                       |
| ---------- | --------- | -------- | ----------------- | ------------------------------------------------------------------------------------------------- |
| token      | STRING    | 32       | PK                | Token de vinculación.                                                                             |
| driver_id  | UUID      |          | FK, NOT NULL      | Identificador del conductor vinculado. Se relaciona con la columna driver_id de la tabla [drivers](#drivers). |
| created_at | TIMESTAMP |          | NOT NULL, DEFAULT | Marca de tiempo de creación del token. Por defecto es la fecha y hora actual.                     |

### vehicles

Almacena la información de los vehículos registrados.

| Columna       | Tipo                                                                                               | Longitud | Restricción       | Descripción                                                                                                                                                                   |
| ------------- | -------------------------------------------------------------------------------------------------- | -------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| vehicle_id    | UUID                                                                                               |          | PK                | Identificador de vehículo.                                                                                                                                                    |
| plate_number  | STRING                                                                                             | 8-12     | NOT NULL, UNIQUE  | Número de placas del vehículo.                                                                                                                                                |
| reg_number    | STRING                                                                                             | 16-22    | NOT NULL, UNIQUE  | Número de registro de tarjeta de circulación del vehículo.                                                                                                                    |
| series_vin    | STRING                                                                                             | 17       | NOT NULL, UNIQUE  | Número de serie del vehículo (VIN).                                                                                                                                           |
| brand         | STRING                                                                                             | 1-60     | NOT NULL          | Marca del vehículo.                                                                                                                                                           |
| model         | STRING                                                                                             | 1-60     | NOT NULL          | Modelo del vehículo.                                                                                                                                                          |
| year          | INT                                                                                                |          | NOT NULL          | Año del vehículo.                                                                                                                                                             |
| type          | ENUM(PASSENGER_CAR, PICKUP, PANEL, VAN, BUS, TRUCK)                                                |          | NOT NULL          | Tipo de vehículo. Puede ser: vehículo de pasajeros, camioneta, panel, van, autobus, camión.                                                                                   |
| status        | ENUM(OPERATIVE, IN_USE, OUT_OF_SERVICE, UNDER_MAINTENANCE, DOCUMENTS_EXPIRED, HELD_BY_AUTHORITIES) |          | NOT NULL, DEFAULT | Estado actual del vehículo. Puede ser: operativo, en uso, fuera de servicio, en mantenimiento, documentación expirada o retenido por las autoridades. Por defecto: operativo. |
| registered_at | TIMESTAMP                                                                                          |          | NOT NULL, DEFAULT | Marca de tiempo de registro del vehículo. Por defecto es la fecha y hora actual.                                                                                              |
| updated_at    | TIMESTAMP                                                                                          |          | ON UPDATE         | Marca de tiempo de actualización del vehículo. Por defecto es la fecha y hora actual.                                                                                         |

### vehicle_services

Almacena la información acerca de los servicios de mantenimiento a los vehículos.

| Columna           | Tipo                                                        | Longitud | Restricción       | Descripción                                                                                                                                 |
| ----------------- | ----------------------------------------------------------- | -------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| service_id        | UUID                                                        |          | PK                | Identificador de servicio.                                                                                                                  |
| vehicle_id        | UUID                                                        |          | FK, NOT NULL      | Identificador del vehículo. Se relaciona con la columna vehicle_id de la tabla [vehicles](#vehicles).                                                    |
| name              | STRING                                                      | 60       | NOT NULL          | Nombre del servicio.                                                                                                                        |
| description       | LONGTEXT                                                    | 500      |                   | Descripción del servicio.                                                                                                                   |
| status            | ENUM(PENDING, IN_PROGRESS, COMPLETED, CANCELLED, DISCARDED) |          | NOT NULL, DEFAULT | Estado actual del servicio de mantenimiento. Puede ser: pendiente, en progreso, completado, cancelado, descartado. Por defecto: pendiente.  |
| date              | DATETIME                                                    |          | NOT NULL          | Fecha y hora en que se realiza el servicio de mantenimiento.                                                                                |
| next_service_date | DATETIME                                                    |          |                   | Fecha y hora estimada para el siguiente servicio de mantenimiento.                                                                          |
| created_by_id     | UUID                                                        |          | NOT NULL          | Identificador del usuario que crea la realización del servicio de mantenimiento. Se relaciona con la columna user_id de la tabla [users](#users).     |
| authorized_by_id  | UUID                                                        |          |                   | Identificador del usuario que autoriza la realización del servicio de mantenimiento. Se relaciona con la columna user_id de la tabla [users](#users). |
| registered_at     | TIMESTAMP                                                   |          | NOT NULL, DEFAULT | Marca de tiempo de registro del servicio. Por defecto es la fecha y hora actual.                                                            |
| updated_at        | TIMESTAMP                                                   |          |                   | Marca de tiempo de actualización del servicio. Por defecto es la fecha y hora actual.                                                       |

### vehicle_event_codes

Define los códigos de eventos de vehículo con descripción y severidad.

| Columna     | Tipo                          | Longitud | Restricción      | Descripción                                                         |
| ----------- | ----------------------------- | -------- | ---------------- | ------------------------------------------------------------------- |
| code        | STRING                        | 12       | PK               | Código de evento.                                                   |
| description | STRING                        | 40       | NOT NULL, UNIQUE | Descripción del evento.                                             |
| severity    | ENUM(INFO, WARNING, CRITICAL) |          | NOT NULL         | Severidad del evento. Puede ser: información, advertencia, crítico. |

### vehicle_events

Almacena la información acerca de los eventos registrados por los dispositivos en los vehículos.


| Columna         | Tipo                   | Longitud | Restricción       | Descripción                                                                                                                                        |
| --------------- | ---------------------- | -------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| event_id        | UUID                   |          | PK                | Identificador de evento.                                                                                                                           |
| code            | STRING                 | 12       | FK, NOT NULL      | Código identificador del tipo de evento generado por el dispositivo. Se relaciona con la columna code de la tabla [vehicle_event_codes](#vehicle_event_codes).             |
| vehicle_id      | UUID                   |          | FK, NOT NULL      | Identificador del vehículo donde está instalado el dispositivo que produjo el evento. Se relaciona con la columna vehicle_id de la tabla [vehicles](#vehicles). |
| position        | GEOGRAPHY(Point, 4326) |          |                   | Coordenadas geográficas donde se originó el evento del vehículo.                                                                                   |
| additional_data | JSON                   |          |                   | Datos complementarios o métricas en formato JSON asociados al evento.                                                                              |
| registered_at   | TIMESTAMP              |          | NOT NULL, DEFAULT | Marca de tiempo de registro del evento. Por defecto es la fecha y hora actual.                                                                     |

### vehicle_devices

Almacena la información acerca de los dispositivos instalados en el vehículo.

| Columna       | Tipo            | Longitud | Restricción       | Descripción                                                                                                                                                                                    |
| ------------- | --------------- | -------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| device_id     | UUID            |          | PK                | Identificador único del dispositivo telemático.                                                                                                                                                |
| vehicle_id    | UUID            |          | FK, NOT NULL      | Identificador del vehículo al que está asignado e instalado el dispositivo. Se relaciona con la columna vehicle_id de la tabla [vehicles](#vehicles).                                                       |
| serial_number | STRING          | 12       | NOT NULL          | Número de serie de fabricación del dispositivo.                                                                                                                                                |
| tag           | STRING          | 16       | NOT NULL          | Etiqueta o identificador alfanumérico visible asignado al dispositivo.                                                                                                                         |
| type          | ENUM(HUB, NODE) |          | NOT NULL          | Tipo de dispositivo telemático o sensor instalado en el vehículo. Puede ser: hub (concentrador que procesa los datos de los sensores), node (dispositivo equipado con sensor, cámara o ambos). |
| battery_level | INT             |          | CHECK             | Nivel porcentual o carga actual de la batería del dispositivo. Debe encontrarse en el rango [0, 100].                                                                                          |
| is_active     | BOOLEAN         |          | NOT NULL, DEFAULT | Indica si el dispositivo se encuentra activo y transmitiendo datos. Por defecto es FALSE.                                                                                                      |
| is_enabled    | BOOLEAN         |          | NOT NULL, DEFAULT | Indica si el dispositivo se encuentra habilitado. Por defecto es TRUE.                                                                                                                         |
| registered_at | TIMESTAMP       |          | NOT NULL, DEFAULT | Marca de tiempo de registro del dispositivo. Por defecto es la fecha y hora actual.                                                                                                            |
| updated_at    | TIMESTAMP       |          | ON UPDATE         | Marca de tiempo de actualización del dispositivo. Por defecto es la fecha y hora actual.                                                                                                       |

### known_locations

Define los lugares conocidos para usarse como puntos de origen y destino en los viajes.

| Columna       | Tipo                    | Longitud | Restricción       | Descripción                                                               |
| ------------- | ----------------------- | -------- | ----------------- | ------------------------------------------------------------------------- |
| location_id   | UUID                    |          | PK                | Identificador de la ubicación.                                            |
| name          | STRING                  | 1-60     | NOT NULL          | Nombre de la ubicación.                                                   |
| type          | STRING                  | 40       |                   | Tipo de la ubicación.                                                     |
| address       | LONG TEXT               | 240      | NOT NULL          | Dirección completa de la ubicación.                                       |
| location_area | GEOMETRY(Polygon, 4326) |          | NOT NULL          | Polígono de la ubicación para usarla con Geocercas.                       |
| registered_at | TIMESTAMP               |          | NOT NULL, DEFAULT | Fecha de registro de la ubicación. Por defecto es la fecha y hora actual. |

### trips

Almacena la información de viajes registrados.

| Columna        | Tipo                                                                                              | Longitud | Restricción       | Descripción                                                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------- | -------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| trip_id        | UUID                                                                                              |          | PK                | Identificador único del viaje registrado.                                                                                                                                              |
| vehicle_id     | UUID                                                                                              |          | FK, NOT NULL      | Identificador del vehículo asignado para realizar el viaje. Se relaciona con la columna vehicle_id de la tabla [vehicles](#vehicles).                                                               |
| driver_id      | UUID                                                                                              |          | FK, NOT NULL      | Identificador del conductor asignado para operar el viaje. Se relaciona con la columna driver_id de la tabla [drivers](#drivers).                                                                  |
| origin_id      | UUID                                                                                              |          | FK, NOT NULL      | Identificador del lugar conocido configurado como punto de origen. Se relaciona con la columna location_id de la tabla [known_locations](#known_locations).                                                |
| destination_id | UUID                                                                                              |          | FK, NOT NULL      | Identificador del lugar conocido configurado como punto de destino. Se relaciona con la columna location_id de la tabla [known_locations](#known_locations).                                               |
| departure_date | DATETIME                                                                                          |          | NOT NULL          | Fecha y hora programada o estimada de salida del viaje.                                                                                                                                |
| arrive_date    | DATETIME                                                                                          |          |                   | Fecha y hora programada o estimada de llegada al destino.                                                                                                                              |
| status         | ENUM(PLANNED, DELAYED, ON_ROUTE, AT_BASE, STOPPED, FINISHED, CANCELLED, ABORTED, GPS_SIGNAL_LOST) |          | NOT NULL          | Estado actual del viaje en el sistema. Puede ser: planeado, retrasado, en ruta, en base, detenido, finalizado, cancelado, abortado, señal GPS perdida. Valor predeterminado: planeado. |
| distance       | NUMERIC                                                                                           | 5,2      |                   | Distancia total recorrida durante el trayecto del viaje en kilómetros.                                                                                                                 |
| average_speed  | NUMERIC                                                                                           | 5,2      |                   | Velocidad promedio registrada durante el viaje en km/h.                                                                                                                                |
| created_at     | TIMESTAMP                                                                                         |          | NOT NULL, DEFAULT | Marca de tiempo de la creación del viaje. Por defecto es la fecha y hora actual.                                                                                                       |
| started_at     | TIMESTAMP                                                                                         |          |                   | Marca de tiempo real de inicio del viaje.                                                                                                                                              |
| finished_at    | TIMESTAMP                                                                                         |          |                   | Marca de tiempo real de finalización o cierre del viaje.                                                                                                                               |

### positions

Almacena los registros de ubicación de los vehículos.

| Campo         | Tipo                   | Longitud | Restricción  | Descripción                                                                                                                 |
| ------------- | ---------------------- | -------- | ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| position_id   | UUID                   |          | PK           | Identificador único del registro de posición.                                                                               |
| vehicle_id    | UUID                   |          | FK, NOT NULL | Identificador del vehículo que registro la posición. Se relaciona con la columna vehicle_id de la tabla [vehicles](#vehicles).           |
| trip_id       | UUID                   |          | FK           | Identificador del viaje al cual corresponde el registro de posición. Se relaciona con la columna trip_id de la tabla [trips](#trips). |
| position      | GEOGRAPHY(Point, 4326) |          | NOT NULL     | Coordenadas geográficas registradas del vehículo en el trayecto.                                                            |
| speed         | NUMERIC                | 5,2      | NOT NULL     | Velocidad instantánea registrada del vehículo en km/h.                                                                      |
| registered_at | TIMESTAMP              |          | NOT NULL     | Marca de tiempo de captura de la posición. Por defecto es la fecha y hora actual.                                           |

### incident_codes

Definir los códigos de incidentes con descripción y severidad.

| Columna     | Tipo                          | Longitud | Restricción      | Descripción                                                               |
| ----------- | ----------------------------- | -------- | ---------------- | ------------------------------------------------------------------------- |
| code        | STRING                        | 12       | PK               | Código de la incidencia.                                                  |
| description | STRING                        | 40       | NOT NULL, UNIQUE | Descripción de la incidencia.                                             |
| severity    | ENUM(INFO, WARNING, CRITICAL) |          | NOT NULL         | Severidad de la incidencia. Puede ser: información, advertencia, crítico. |

### incidents

Almacena la información de las incidencias reportadas durante un viaje.

| Campo               | Tipo                                       | Longitud | Restricción       | Descripción                                                                                                                                                              |
| ------------------- | ------------------------------------------ | -------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| incident_id         | UUID                                       |          | PK                | Identificador único de la incidencia reportada.                                                                                                                          |
| trip_id             | UUID                                       |          | FK, NOT NULL      | Identificador del viaje durante el cual ocurrió la incidencia. Se relaciona con la columna trip_id de la tabla [trips](#trips).                                                    |
| code                | STRING                                     | 12       | FK, NOT NULL      | Código de referencia del catálogo de tipos de incidencia. Se relaciona con la columna code de la tabla [incident_codes](#incident_codes).                                                   |
| status              | ENUM(OPEN, IN_REVISION, CLOSED, DISCARDED) |          | NOT NULL, DEFAULT | Estado actual de atención o resolución de la incidencia. Puede ser: abierto, en revisión, cerrado, descartado. Por defecto: abierto.                                     |
| position            | GEOGRAPHY(Point, 4326)                     |          |                   | Coordenadas geográficas donde ocurrió la incidencia.                                                                                                                     |
| description         | LONGTEXT                                   | 500      | NOT NULL          | Descripción detallada de los hechos ocurridos en la incidencia.                                                                                                          |
| comments            | LONGTEXT                                   | 500      |                   | Comentarios u observaciones de seguimiento por parte del agente.                                                                                                         |
| related_incident_id | UUID                                       |          | FK, NOT NULL      | Identificador de la incidencia vinculada o relacionada para dar seguimiento. Se relaciona con la columna incident_id de la misma tabla.                                  |
| registered_at       | TIMESTAMP                                  |          | NOT NULL, DEFAULT | Marca de tiempo de registro de la incidencia. Por defecto es la fecha y hora actual.                                                                                     |
| reviewed_at         | TIMESTAMP                                  |          |                   | Marca de tiempo en que la incidencia fue revisada por el agente.                                                                                                         |
| closed_at           | TIMESTAMP                                  |          |                   | Marca de tiempo en que la incidencia fue cerrada o resuelta.                                                                                                             |
| created_by_id       | UUID                                       |          | FK                | Identificador del usuario que registró la incidencia. Se relaciona con la columna user_id de la tabla [users](#users). Si es nulo, se asume que el sistema registró la incidencia. |
| reviewed_by_id      | UUID                                       |          | FK                | Identificador del agente asignado para atender la incidencia. Se relaciona con la columna user_id de la tabla [users](#users).                                                     |

### incident_media

Almacena la informción de las evidencias multimedia asociadas a un incidente.

| Campo         | Tipo               | Longitud | Restricción  | Descripción                                                                                                                    |
| ------------- | ------------------ | -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| media_id      | UUID               |          | PK           | Identificador único de la evidencia multimedia.                                                                                |
| incident_id   | UUID               |          | FK, NOT NULL | Identificador de la incidencia vinculada al archivo multimedia. Se relaciona con la columna incident_id de la tabla [incidents](#incidents). |
| file_url      | STRING             |          | NOT NULL     | Identificador o ruta del archivo en el repositorio de almacenamiento.                                                          |
| type          | ENUM(IMAGE, VIDEO) |          | NOT NULL     | Tipo de evidencia multimedia capturada. Puede ser de tipo imagen o vídeo.                                                      |
| file_metadata | JSON               |          | NOT NULL     | Metadatos del archivo de evidencia multimedia.                                                                                 |
| captured_at   | TIMESTAMP          |          | NOT NULL     | Marca de tiempo en la que fue capturada la evidencia multimedia.                                                               |
| uploaded_at   | TIMESTAMP          |          |              | Marca de tiempo en la que se completó la subida del archivo al servidor.                                                       |
