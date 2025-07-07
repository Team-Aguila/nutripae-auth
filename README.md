# PAE-AUTH: Sistema de Autenticación y Autorización

Sistema completo de autenticación y autorización construido con **FastAPI** que implementa un control de acceso basado en roles (RBAC) con funcionalidades avanzadas de gestión de usuarios, roles, permisos e invitaciones.

## 🚀 Características Principales

### 🔐 **Autenticación Robusta**
- **Login seguro** con JWT tokens
- **Registro por código de invitación**
- **Recuperación de contraseña** por email
- **Cambio de contraseña** para usuarios autenticados
- **Validación de contraseñas fuertes**
- **Gestión de sesiones** con expiración automática

### 👥 **Gestión Completa de Usuarios**
- ✅ **Crear usuarios** (con permisos de admin)
- ✅ **Listar usuarios** (paginado y filtrable)
- ✅ **Ver detalles** de usuarios
- ✅ **Editar usuarios** (con auditoría completa)
- ✅ **Eliminación lógica** de usuarios
- ✅ **Filtros avanzados** por estado, rol, búsqueda de texto

### 🛡️ **Sistema de Roles y Permisos**
- ✅ **CRUD completo de roles**
- ✅ **Asignación múltiple** de permisos a roles
- ✅ **Catálogo de permisos** visualizable
- ✅ **Control granular** de acceso
- ✅ **Validación de dependencias** (no se puede eliminar rol con usuarios)

### 📨 **Sistema de Invitaciones**
- ✅ **Generación de códigos únicos**
- ✅ **Asignación previa de roles**
- ✅ **Expiración automática**
- ✅ **Gestión de estados** (Pendiente, Aceptada, Expirada, Cancelada)
- ✅ **Cancelación manual** de invitaciones

### 🔍 **Autorización Externa**
- ✅ **Endpoint de verificación** para otros módulos
- ✅ **Consulta de permisos** de usuario
- ✅ **Integración simple** con otros servicios

### 📊 **Auditoría y Monitoreo**
- ✅ **Log completo** de todas las acciones
- ✅ **Seguimiento de cambios** en usuarios y roles
- ✅ **Métricas con Prometheus**
- ✅ **Timestamps automáticos**

## 🏗️ Arquitectura

El sistema sigue los principios de **Arquitectura Limpia (Clean Architecture)**:

```
📦 Estructura del Proyecto
├── 🎯 controllers/     # Capa de Presentación (API endpoints)
├── 🔧 services/        # Capa de Aplicación (lógica de negocio)
├── 🗃️ models/          # Capa de Dominio (entidades)
├── 📊 repositories/    # Capa de Infraestructura (acceso a datos)
├── 🔒 schemas/         # Validación y serialización (Pydantic)
├── ⚙️ core/           # Configuración y utilidades transversales
└── 🗄️ db/            # Configuración de base de datos
```

## 📋 Requerimientos Funcionales Implementados

### **RF 1.1: Gestión de Usuarios** ✅
- **RF 1.1.1**: Registrar Nuevo Usuario ✅
- **RF 1.1.2**: Consultar Detalles de Usuario ✅
- **RF 1.1.3**: Modificar Datos de Usuario ✅
- **RF 1.1.4**: Eliminación Lógica de Usuario ✅
- **RF 1.1.5**: Listado de Usuarios ✅

### **RF 1.2: Gestión de Roles** ✅
- **RF 1.2.1**: Crear Nuevo Rol ✅
- **RF 1.2.2**: Consultar Roles ✅
- **RF 1.2.3**: Consultar Detalle de Rol ✅
- **RF 1.2.4**: Modificar Rol ✅
- **RF 1.2.5**: Eliminar Rol ✅

### **RF 1.3: Gestión de Permisos** ✅
- **RF 1.3.1**: Consultar Catálogo de Permisos ✅

### **RF 1.4: Gestión de Códigos de Invitación** ✅
- **RF 1.4.1**: Generar Código de Invitación ✅
- **RF 1.4.2**: Consultar y Gestionar Invitaciones ✅

### **RF 2.1: Autenticación de Usuario** ✅
- **RF 2.1.1**: Proceso de Inicio de Sesión ✅

### **RF 2.2: Recuperación de Contraseña** ✅
- **RF 2.2.1**: Solicitar restablecimiento ✅
- **RF 2.2.2**: Restablecer Contraseña ✅

### **RF 2.3: Cambio de Contraseña** ✅

### **RF 2.4: Gestión de Sesiones Seguras** ✅

### **RF 2.5: Registro por Invitación** ✅
- **RF 2.5.1**: Formulario de Registro por Invitación ✅
- **RF 2.5.2**: Validación y Creación de Cuenta ✅
- **RF 2.5.3**: Manejo de Errores de Registro ✅

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para manejo de base de datos
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos y configuración
- **JWT (Jose)** - Autenticación basada en tokens
- **Bcrypt** - Hashing seguro de contraseñas
- **Prometheus** - Métricas y monitoreo

## 🚀 Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone <repo-url>
cd pae-auth
```

### 2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar variables de entorno**
Crear archivo `.env.development`:
```env
# Base de datos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=pae_auth
DB_HOST=localhost
DB_HOST_PORT=5432

# JWT
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin por defecto
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

### 5. **Configurar base de datos**
```bash
# Asegurar que PostgreSQL esté corriendo
# Crear la base de datos
createdb pae_auth
```

### 6. **Ejecutar la aplicación**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación de API

Una vez ejecutada la aplicación, acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Permisos del Sistema

### **Permisos de Usuario**
- `usuario.crear` - Crear nuevos usuarios
- `usuario.ver` - Ver detalles de usuarios
- `usuario.ver_lista` - Listar usuarios
- `usuario.editar` - Editar usuarios
- `usuario.eliminar` - Eliminar usuarios lógicamente
- `user:read_own` - Ver perfil propio
- `user:update_own` - Actualizar perfil propio

### **Permisos de Rol**
- `rol.crear` - Crear nuevos roles
- `rol.ver` - Ver detalles de roles
- `rol.ver_lista` - Listar roles
- `rol.editar` - Editar roles
- `rol.eliminar` - Eliminar roles

### **Permisos de Permisos**
- `permiso.ver_lista` - Ver catálogo de permisos

### **Permisos de Invitación**
- `invitacion.generar` - Generar códigos de invitación
- `invitacion.ver_lista` - Ver y gestionar invitaciones

## 👥 Roles Predefinidos

### **Super Admin**
- Todos los permisos del sistema
- Gestión completa de usuarios, roles y permisos

### **Project Admin**
- Gestión de usuarios dentro del proyecto
- Creación y gestión de invitaciones
- Gestión de roles (ver y asignar)

### **Basic User**
- Acceso de solo lectura a su perfil
- Actualización de su propia información

## 🔍 Autorización Externa

### **Endpoint de Verificación**
```http
POST /authorization/check-authorization
Authorization: Bearer <token>
Content-Type: application/json

{
    "endpoint": "recursos-humanos/empleados",
    "method": "GET",
    "required_permissions": ["empleado.ver", "proyecto.acceder"]
}
```

**Respuesta:**
```json
{
    "authorized": true,
    "user_id": 123,
    "user_email": "user@example.com",
    "user_permissions": ["empleado.ver", "proyecto.acceder", "..."],
    "required_permissions": ["empleado.ver", "proyecto.acceder"],
    "missing_permissions": [],
    "endpoint": "recursos-humanos/empleados",
    "method": "GET"
}
```

### **Consulta de Permisos**
```http
GET /authorization/user-permissions
Authorization: Bearer <token>
```

## 📊 Ejemplos de Uso

### **1. Crear una invitación**
```http
POST /invitations/
Authorization: Bearer <admin-token>
Content-Type: application/json

{
    "email": "nuevo@example.com",
    "role_ids": [2, 3],
    "expires_at": "2024-12-31T23:59:59"
}
```

### **2. Registrarse con código de invitación**
```http
POST /auth/register-by-invitation
Content-Type: application/json

{
    "invitation_code": "ABC123XYZ0",
    "user_data": {
        "email": "nuevo@example.com",
        "full_name": "Nuevo Usuario",
        "username": "nuevo_user",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
}
```

### **3. Listar usuarios con filtros**
```http
GET /users/?skip=0&limit=10&status_filter=1&search=juan
Authorization: Bearer <admin-token>
```

## 🐛 Troubleshooting

### **Error de base de datos**
- Verificar que PostgreSQL esté corriendo
- Confirmar credenciales en `.env.development`
- Verificar que la base de datos existe

### **Error de autenticación**
- Verificar que `SECRET_KEY` esté configurada
- Confirmar que el token no haya expirado
- Verificar permisos del usuario

### **Error de importación**
- Confirmar que todas las dependencias estén instaladas
- Verificar la estructura de directorios
- Revisar imports circulares

## 🤝 Contribución

1. Fork el proyecto
2. Crear branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte y preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación en `/docs`

---

**PAE-AUTH** - Sistema de Autenticación y Autorización Robusto 🔐
