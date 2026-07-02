# SaludMente Comunitaria

Sistema web para la gestión de atención psicológica comunitaria. Permite administrar beneficiarios, sesiones, seguimientos, usuarios y generar reportes mediante una API desarrollada con FastAPI.

## Estructura del proyecto

```text
backend/app/
│── config/
│── controller/
│── entity/
│── repository/
│── schemas/
└── service/
```

## Funcionalidades

* Gestión de beneficiarios.
* Gestión de sesiones.
* Gestión de seguimientos.
* Administración de usuarios.
* Reportes.
* Inicio de sesión con autenticación.

## Requisitos

* Python 3.11 o superior
* MySQL
* pip

## Ejecutar el backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Documentación de la API:

```text
http://127.0.0.1:8000/docs
```

## Ejecutar el frontend

Abrir el archivo:

```text
frontend/index.html
```

## Base de datos

El proyecto utiliza MySQL.

Cadena de conexión por defecto:

```text
mysql+pymysql://root:12345@localhost:3306/saludmente_db
```

Si desea utilizar otra conexión, configure la variable:

```bash
set DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/saludmente_db
```

## Credenciales de prueba

```text
Correo: admin@sistema.com
Contraseña: admin123
```

## Endpoints principales

```text
POST /auth/login

Usuarios
GET    /usuarios/
POST   /usuarios/
PUT    /usuarios/{id}
DELETE /usuarios/{id}

Beneficiarios
GET    /beneficiarios/
POST   /beneficiarios/
PUT    /beneficiarios/{id}
DELETE /beneficiarios/{id}

Sesiones
GET    /sesiones/
POST   /sesiones/
PUT    /sesiones/{id}
DELETE /sesiones/{id}

Seguimientos
GET    /seguimientos/
POST   /seguimientos/
PUT    /seguimientos/{id}
DELETE /seguimientos/{id}

Reportes
GET /reportes/resumen
GET /reportes/beneficiarios-por-estado
GET /reportes/sesiones-por-estado
GET /reportes/carga-terapeutas
```

Los endpoints protegidos requieren un token:

```text
Authorization: Bearer <token>
```

## Reglas de negocio

* No se pueden registrar sesiones para beneficiarios con casos cerrados.
* Solo usuarios activos con rol **admin** o **terapeuta** pueden atender sesiones.
* Un terapeuta no puede tener dos sesiones en la misma fecha y hora.
* Al registrar una sesión o seguimiento, el caso pasa a **en seguimiento**.
* Los seguimientos pueden tener prioridad baja, media o alta.

## Principios SOLID

* **SRP:** cada capa tiene una única responsabilidad.
* **OCP:** es posible agregar nuevos módulos sin modificar los existentes.
* **LSP:** los servicios utilizan repositorios con operaciones consistentes.
* **ISP:** cada controlador expone únicamente las operaciones necesarias.
* **DIP:** los controladores dependen de servicios y no directamente de la base de datos.

## Errores comunes

### `link.exe not found`

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Si el problema continúa, utilice Python 3.11 o 3.12 y vuelva a crear el entorno virtual.

### `ERR_CONNECTION_REFUSED`

Verifique que el backend esté ejecutándose:

```bash
cd backend
uvicorn app.main:app --reload
```
