import os
import random
import string
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_microsoft_identity import requires_auth, AuthError, validate_scope, auth_service
from dependencies.auth_dependency import get_current_user_oid
from dto.ResponseRequest import ResponseRequest
from dto.UsuariosDTO import UsuariosUpdateBase
# from dto.validation_error import ValidationError
from pathlib import Path
# from repository import UsuariosRepository
from services import UsuariosService
from database.database import DbSession
from dto.UsuariosDTO import UsuariosBase, UsuariosCreateBase
import msal
from fastapi.responses import JSONResponse
from fastapi import status
import json
import requests
import jwt

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

required_scope = 'access_as_user'
SCOPE = ["https://graph.microsoft.com/.default"]

# def configure_scopes():
#     file = Path('settings.json').absolute()
#     if not file.exists():
#         raise Exception('settings.json file not found, please see settings_template.json')
#     with open(file) as fin:
#         settings = json.load(fin)
#         global SCOPE
#         SCOPE.append(settings.get('scope', []))
#         print(f'Scopes configured: {SCOPE}')
#         global required_scope
#         required_scope = settings.get('required_scope', '')
#         if not required_scope:
#             raise Exception('No scopes defined in settings.json, please see settings_template.json')


# def get_msal_app():
#     return msal.ConfidentialClientApplication(
#         os.getenv("client_id"),
#         authority=f"https://login.microsoftonline.com/{os.getenv("tenant_id")}",
#         client_credential=os.getenv("client_secret")
#     )

# def get_access_token():
#     app = get_msal_app()
#     result = app.acquire_token_for_client(scopes=SCOPE)
#     if "access_token" in result:
#         return result["access_token"]
#     else:
#         raise Exception("Could not get access token")
    
# @router.get("/menu")
# def listar_menu_x_rol(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     try:
#         menu = MenuService.listar_menu_x_rol(user_oid, db)
#         return menu
#     except HTTPException as e:
#         print(f"HTTPException: {e.detail}")
#         raise e
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
    

#     # return MenuService.listar_menu_x_rol(ids_rol, db)


# @router.get("/validar_acceso")
# def validar_acceso(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     try:

#         usuario = UsuariosRepository.obtener_por_guid_msft(user_oid, db)
#         respuesta = ResponseRequest(solicitud_exitosa=True)
#         if usuario == None:
#             respuesta.solicitud_exitosa = False
#             respuesta.mensaje = "El usuario no tiene acceso al sistema"
#         return JSONResponse(
#             content=respuesta.dict(),
#             status_code=status.HTTP_401_UNAUTHORIZED if not respuesta.solicitud_exitosa else status.HTTP_200_OK
#         )
#     except HTTPException as e:
#         print(f"HTTPException: {e.detail}")
#         raise e
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
    

#     # return MenuService.listar_menu_x_rol(ids_rol, db)




@router.post("")
def crear_usuario(usuario: UsuariosCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = UsuariosService.crear_usuario(usuario, db)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_409_CONFLICT
            )
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("")
def listar_usuarios(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return UsuariosService.listar_usuarios(db)
    # configure_scopes()

    # """
    # Lista los usuarios disponibles en Microsoft Entra (Azure AD) usando Microsoft Graph API.
    # """
    # try:
    #     access_token = get_access_token()
    #     url = "https://graph.microsoft.com/v1.0/users"
    #     headers = {
    #         "Authorization": f"Bearer {access_token}"
    #     }
    #     response = requests.get(url, headers=headers)
    #     users = []
    #     while url:  # Mientras haya más páginas de resultados
    #         response = requests.get(url, headers=headers)
    #         if response.status_code == 200:
    #             data = response.json()
    #             users.extend(data.get("value", []))  # Añadir los usuarios actuales a la lista
                
    #             # Verificar si hay más páginas
    #             url = data.get('@odata.nextLink')  # Obtener el siguiente enlace de la página
                
    #             # Detener si ya tenemos 500 usuarios
    #             if len(users) >= 10000:
    #                 return users[:10000]  # Devolver solo los primeros 500 usuarios
    #         else:
    #             raise Exception(f"Error fetching users: {response.status_code} - {response.text}")
        
    #     return users
    # except Exception as e:
    #     print(f"Error fetching users: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))


def random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))



@router.get("/msf")
def listar_usuarios(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    # configure_scopes()
    try:
        group_id = os.getenv("grupo_usuarios")
        access_token = get_access_token()  # Debes tener esta función implementada
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$top=500"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        usuarios_activos = []
        usuarios_registrados = UsuariosService.listar_usuarios(db)
        excluir_ids_usuarios_msft = []
        for dto in usuarios_registrados:
            excluir_ids_usuarios_msft.append(str(dto.guid_msft))

        while url and len(usuarios_activos) < 500:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            data = response.json()
            miembros = data.get("value", [])
            # Filtrar solo usuarios activos y excluir los IDs indicados
            for u in miembros:
                if (
                    u["@odata.type"] == "#microsoft.graph.user"
                    and u.get("accountEnabled", True)
                    and u.get("id") not in excluir_ids_usuarios_msft
                ):
                    print(u)
                    usuarios_activos.append(u)
                    if len(usuarios_activos) >= 500:
                        break
            url = data.get("@odata.nextLink")
        return usuarios_activos[:500]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



    # exclude_ids = []
    # usuarios = UsuariosService.listar_usuarios(db)

    # for dto in usuarios:
    #     exclude_ids.append(str(dto.guid_msft))
    # """
    # Lista los usuarios disponibles en Microsoft Entra (Azure AD) usando Microsoft Graph API.
    # """
    # try:
    #     access_token = get_access_token()
    #     url = "https://graph.microsoft.com/v1.0/users"
    #     headers = {
    #         "Authorization": f"Bearer {access_token}"
    #     }
    #     response = requests.get(url, headers=headers)
    #     users = []
    #     while url:  # Mientras haya más páginas de resultados
    #         response = requests.get(url, headers=headers)
    #         if response.status_code == 200:
    #             data = response.json()
    #             filtered_users = [user for user in data.get("value", []) if user["id"] not in exclude_ids]
    #             users.extend(filtered_users)
    #             # Verificar si hay más páginas
    #             url = data.get('@odata.nextLink')  # Obtener el siguiente enlace de la página
                
    #             # Detener si ya tenemos 500 usuarios
    #             if len(users) >= 10000:
    #                 return users[:10000]  # Devolver solo los primeros 500 usuarios
    #         else:
    #             raise Exception(f"Error fetching users: {response.status_code} - {response.text}")
        
    #     return users
    # except Exception as e:
    #     print(f"Error fetching users: {e}")
    #     raise HTTPException(status_code=500, detail=str(e))

def get_access_token():
    app = get_msal_app()
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not get access token")

def get_msal_app():
    return msal.ConfidentialClientApplication(
        os.getenv("client_id"),
        authority=f"https://login.microsoftonline.com/{os.getenv('tenant_id')}",
        client_credential=os.getenv("client_secret")
    )



@router.get("/validar_correo_grupo/{correo}")
def validar_correo_en_grupo(correo: str, user_oid: str = Depends(get_current_user_oid)):
    try:
        access_token = get_access_token()
        group_id = os.getenv("grupo_usuarios")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        #Buscar el usuario en Azure AD por correo
        search_url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{correo}' or userPrincipalName eq '{correo}'"
        search_response = requests.get(search_url, headers=headers)
        
        if search_response.status_code != 200:
            raise HTTPException(status_code=search_response.status_code, detail=search_response.text)
        
        search_data = search_response.json()
        usuarios_encontrados = search_data.get("value", [])
        
        if len(usuarios_encontrados) == 0:
            return {
                "existe": False,
                "mensaje": "Usuario no encontrado en Azure AD"
            }
        
        usuario = usuarios_encontrados[0]
        user_id = usuario.get("id")
        
        #Verificar si el usuario es miembro del grupo
        check_membership_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/{user_id}"

        # UsuariosService.agregar_usuario_a_grupo(user_id, access_token)
        membership_response = requests.get(check_membership_url, headers=headers)
        
        if membership_response.status_code == 200:
            # El usuario es miembro del grupo
            return {
                "existe": True,
                "guid_msft": user_id,
                "displayName": usuario.get("displayName"),
                "mail": usuario.get("mail"),
                "userPrincipalName": usuario.get("userPrincipalName")
            }
        elif membership_response.status_code == 404:
            # El usuario existe en Azure AD pero no es miembro del grupo
            return {
                "existe": False,
                "mensaje": f"El usuario '{usuario.get('displayName')}' existe en Azure AD pero no pertenece al grupo corporativo"
            }
        else:
            raise HTTPException(status_code=membership_response.status_code, detail=membership_response.text)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/validar_usuario/{guid}")
def validar_usuario_corporativo(guid: str, datos_validacion: dict, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = UsuariosService.validar_usuario_corporativo(
            guid=guid,
            guid_msft=datos_validacion.get('guid_msft'),
            correo=datos_validacion.get('email'),
            nombre=datos_validacion.get('nombre'),
            db=db
        )
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{guid}")
def obtener_usuario_para_edicion(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    usuario = UsuariosService.obtener_usuario_para_edicion(guid, db)
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario


@router.put("/{guid}")
def actualizar_usuario(guid: str, payload: UsuariosUpdateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = UsuariosService.actualizar_usuario(guid, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Usuario no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)