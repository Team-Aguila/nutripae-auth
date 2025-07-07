from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from core.config import settings
from utils import PrometheusMiddleware, metrics, setting_otlp
import logging
from controllers import (
    auth_controller, 
    project_controller,
    user_controller,
    role_controller,
    permission_controller,
    invitation_controller,
    authorization_controller,
    parametric_controller
)
from db.session import SessionLocal
from db.seeder import seed_db
import uvicorn
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar la aplicación
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    yield
    # Se ejecuta al apagar la aplicación (si es necesario)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="NutriPAE-AUTH: Autenticación y Autorización",
        version="1.0.0",
        routes=app.routes,
    )
    
    # Define the security scheme for JWT Bearer tokens
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token obtained from the /auth/login endpoint"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(PrometheusMiddleware, app_name=settings.APP_NAME)
app.add_route("/metrics", metrics)
# Setting OpenTelemetry exporter
setting_otlp(app, settings.APP_NAME, settings.OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
# Set custom OpenAPI schema
app.openapi = custom_openapi

# Rutas de autenticación
app.include_router(
    auth_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/auth", 
    tags=["Authentication"]
)

# Rutas de gestión de usuarios
app.include_router(
    user_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/users", 
    tags=["User Management"]
)

# Rutas de gestión de roles
app.include_router(
    role_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/roles", 
    tags=["Role Management"]
)

# Rutas de gestión de permisos
app.include_router(
    permission_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/permissions", 
    tags=["Permission Management"]
)

# Rutas de gestión de invitaciones
app.include_router(
    invitation_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/invitations", 
    tags=["Invitation Management"]
)

# Rutas de datos paramétricos
app.include_router(
    parametric_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/parametric", 
    tags=["Parametric Data"]
)

# Rutas de autorización externa
app.include_router(
    authorization_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/authorization", 
    tags=["External Authorization"]
)

# Rutas de proyectos (existente)
app.include_router(
    project_controller.router, 
    prefix=f"{settings.API_PREFIX_STR}/projects", 
    tags=["Project Management"]
)

@app.get(f"{settings.API_PREFIX_STR}", tags=["Root"])
def api_root():
    return {
        "message": "Bienvenido a NutriPAE-AUTH",
        "description": "Autenticación y Autorización",
        "version": "1.0.0",
        "docs_url": "/docs",
        "features": [
            "Autenticación JWT",
            "Gestión de Usuarios",
            "Roles y Permisos Granulares",
            "Sistema de Invitaciones",
            "Datos Paramétricos",
            "Autorización Externa",
            "Auditoría Completa",
            "Métricas con Prometheus"
        ]
    }

@app.get("/", tags=["Root"])
def root():
    return {"status": "healthy", "service": "pae-auth"}

if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)