from controllers import SolicitudesAprobacionController, ViajesController
import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from controllers import UsuariosController
from controllers import RolesController
from controllers import ProgramasController
from controllers import FlujosAprobacionController
from controllers import FlujosAprobacionController
from controllers import ModalitiesController
from controllers import DocumentsApprovalController
from controllers import PadsController
from controllers import ImplementerTypesController
from controllers import DocumentTypes
from controllers import ImplementersController
from controllers import PidsControllerss
from controllers import PersonsController
from controllers import CapacityAssessmentsStatesController
from controllers import DocumentsTypesAgreementsController
from controllers import CapacityAssessmentsController
from controllers import PreviousStudiesController


from fastapi.middleware.cors import CORSMiddleware
import json
from starlette.staticfiles import StaticFiles
from pathlib import Path
from fastapi_microsoft_identity import initialize 
from jose import jwt
from functools import lru_cache
import requests


@lru_cache
def _get_auth_settings():
   

    tenant_id = os.getenv("tenant_id")
    client_id = os.getenv("client_id")
    required_scope = os.getenv("required_scope")

    if not tenant_id or not client_id:
        raise Exception('tenant_id/client_id not found in settings.json')

    return {
        'tenant_id': tenant_id,
        'client_id': client_id,
        'required_scope': required_scope
    }


@lru_cache
def _get_jwks(tenant_id: str):
    discovery_url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'
    response = requests.get(discovery_url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No fue posible obtener llaves de Azure AD')
    return response.json()


def _has_required_scope_or_role(claims: dict, required_scope: str) -> bool:
    if not required_scope:
        return True

    scopes = claims.get('scp', '')
    roles = claims.get('roles', [])

    if isinstance(scopes, str) and required_scope.lower() in [s.lower() for s in scopes.split()]:
        return True

    if isinstance(roles, list) and required_scope.lower() in [r.lower() for r in roles]:
        return True

    return False


def _is_public_download_request(request: Request) -> bool:
    if request.method.upper() != 'GET':
        return False

    path = request.url.path.lower()
    public_download_markers = [
        '/soporte/',
        '/documento',
        '/archivo/',
        '/facturas/'
    ]

    return any(marker in path for marker in public_download_markers)


def require_authenticated_user(request: Request):
    if _is_public_download_request(request):
        return

    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')

    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header must be 'Bearer <token>'")

    token = parts[1]
    settings = _get_auth_settings()
    tenant_id = settings['tenant_id']
    client_id = settings['client_id']
    required_scope = settings['required_scope']

    try:
        unverified_header = jwt.get_unverified_header(token)
        unverified_claims = jwt.get_unverified_claims(token)

        jwks = _get_jwks(tenant_id)
        rsa_key = {}
        for key in jwks.get('keys', []):
            if key.get('kid') == unverified_header.get('kid'):
                rsa_key = {
                    'kty': key.get('kty'),
                    'kid': key.get('kid'),
                    'use': key.get('use'),
                    'n': key.get('n'),
                    'e': key.get('e')
                }
                break

        if not rsa_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No se encontró llave pública válida para el token')

        token_audience = os.getenv('token_audience', '').strip()
        token_version = unverified_claims.get('ver', '2.0')
        if token_version == '1.0':
            audience = token_audience or f'api://{client_id}'
            issuer = f'https://sts.windows.net/{tenant_id}/'
        else:
            audience = token_audience or client_id
            issuer = f'https://login.microsoftonline.com/{tenant_id}/v2.0'

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=audience,
            issuer=issuer
        )

        if not _has_required_scope_or_role(payload, required_scope):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token sin scope/rol requerido')

        request.state.user_claims = payload

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Token inválido: {str(e)}')

def register_routes(app: FastAPI):
    # app.include_router(PruebaController.router)
    auth_dependency = [Depends(require_authenticated_user)]
    app.include_router(UsuariosController.router, dependencies=auth_dependency)
    app.include_router(RolesController.router, dependencies=auth_dependency)
    app.include_router(ProgramasController.router, dependencies=auth_dependency)
    app.include_router(FlujosAprobacionController.router, dependencies=auth_dependency)
    app.include_router(SolicitudesAprobacionController.router, dependencies=auth_dependency)
    app.include_router(ViajesController.router, dependencies=auth_dependency)
    app.include_router(DocumentsApprovalController.router, dependencies=auth_dependency)
    app.include_router(PadsController.router, dependencies=auth_dependency)
    app.include_router(ImplementerTypesController.router, dependencies=auth_dependency)
    app.include_router( ModalitiesController.router  , dependencies=auth_dependency)
    app.include_router( DocumentTypes.router , dependencies=auth_dependency)
    app.include_router( ImplementersController.router , dependencies=auth_dependency)
    app.include_router( PidsControllerss.router , dependencies=auth_dependency)
    app.include_router(CapacityAssessmentsStatesController.router, dependencies=auth_dependency)
    app.include_router( PersonsController.router , dependencies=auth_dependency)#15
    
    app.include_router( DocumentsTypesAgreementsController.router , dependencies=auth_dependency)#16
    app.include_router( CapacityAssessmentsStatesController.router, dependencies=auth_dependency)#17
    app.include_router( CapacityAssessmentsController.router , dependencies=auth_dependency)#18
    app.include_router(PreviousStudiesController.router , dependencies=auth_dependency)#19
    
    app.include_router( CapacityAssessmentsController.router , dependencies=auth_dependency)#16
    
    

def register_middlewares(app: FastAPI):
    # Register CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure(app: FastAPI):
    configure_api_keys()
    register_middlewares(app)
    register_routes(app)
    configure_fake_data()

def configure_api_keys():
    configure_auth(os.getenv('tenant_id'), os.getenv('client_id'))




def configure_auth(tenant_id, client_id):
    initialize(tenant_id, client_id)
    # This is used to configure Microsoft Identity authentication
    # If you want to use this, you need to set up an app in Azure AD
    # and provide the client ID and tenant ID in settings.json
    # initialize(
    #     api,
    #     client_id='your-client-id',
    #     tenant_id='your-tenant-id',
    #     redirect_uri='http://localhost:8000/auth/callback'
    # )

def configure_fake_data():
    # This was added to make it easier to test the weather event reporting
    # We have /api/reports but until you submit new data each run, it's missing
    # So this will give us something to start from.
    pass  # Doesn't work on Ubuntu under gunicorn
    # try:
    #     loc = Location(city="Portland", state="OR", country="US")
    #     asyncio.run(report_service.add_report("Misty sunrise today, beautiful!", loc))
    #     asyncio.run(report_service.add_report("Clouds over downtown.", loc))
    # except:
    #     print("NOTICE: Add default data not supported on this system (usually under uvicorn on linux)")

