import os
from fastapi import HTTPException

from sqlalchemy.orm import Session
from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from exceptions import PruebaCreationError, PruebaNotFoundError
import logging
from dto.UsuariosDTO import UsuariosBase, UsuariosCreateBase, UsuariosEdicionBase, UsuariosUpdateBase
from repository import UsersProgramsRepository, UsuariosRepository
from dto.ResponseRequest import ResponseRequest
from pathlib import Path
import json
import msal
import requests
from typing import List, Optional, TypedDict
import bcrypt
from entity.users import Users

class InvitacionResponse(TypedDict):
    registro_exitoso: bool
    user_id: Optional[str]
    mensaje: str

SCOPE = ["https://graph.microsoft.com/.default"]


def agregar_usuario_a_grupo(guid: str, access_token: str):
    group_id = (os.getenv("grupo_usuarios") or "").strip()

    if not group_id:
        raise HTTPException(status_code=500, detail="La variable grupo_usuarios no esta configurada")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    check_membership_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/{guid}"
    membership_response = requests.get(check_membership_url, headers=headers)

    if membership_response.status_code == 200:
        return {
            "agregado": False,
            "guid_msft": guid,
            "mensaje": "El usuario ya pertenece al grupo corporativo"
        }

    if membership_response.status_code != 404:
        raise HTTPException(status_code=membership_response.status_code, detail=membership_response.text)

    add_member_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{guid}"
    }
    add_response = requests.post(add_member_url, headers=headers, json=payload)

    if add_response.status_code in (200, 204):
        return {
            "agregado": True,
            "guid_msft": guid,
            "mensaje": "Usuario agregado correctamente al grupo corporativo"
        }

    if add_response.status_code == 400:
        raise HTTPException(
            status_code=400,
            detail="No fue posible agregar el usuario al grupo. Verifique que el guid exista en Azure AD y sea un directory object valido."
        )

    raise HTTPException(status_code=add_response.status_code, detail=add_response.text)
 
def listar_usuarios(db: Session)-> list[UsuariosBase]:
    try:
        usuarios = UsuariosRepository.listar(db)
        usuarios_dtos = [
            UsuariosBase(
                guid=usuario.guid,
                guid_msft=usuario.guid_msft,
                first_name=usuario.first_name,
                last_name=usuario.last_name,
                identification_type=usuario.identification_type,
                identification_number=usuario.identification_number,
                email=usuario.email,
                is_active=usuario.is_active,
                other_name=usuario.other_name,
                other_last_name=usuario.other_last_name,
                position=usuario.position,
                full_name=f"{usuario.first_name} {usuario.other_name or ''} {usuario.last_name} {usuario.other_last_name or ''}".strip()
            )
            for usuario in usuarios
        ]
        return usuarios_dtos
    except Exception as e:
        logging.error(f"Failed to list usuarios: {str(e)}")
        raise PruebaNotFoundError(str(e))

def get_msal_app():
    tenant_id = os.getenv("tenant_id")
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    return msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret
    )
    
def get_access_token():
    app = get_msal_app()
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not get access token")
    
def obtener_usuario_entra_por_correo(correo: str) -> Optional[dict]:
    try:
        access_token = get_access_token()
        url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{correo}' or userPrincipalName eq '{correo}'"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get("value", [])
            if usuarios:
                return usuarios[0]
            return None
        logging.error(f"Error al buscar usuario en Entra ID: {response.text}")
        return None
    except Exception as e:
        logging.error(f"Error al buscar usuario en Entra ID: {str(e)}")
        return None



def crear_usuario(usuario: UsuariosCreateBase, db: Session) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        correo_usuario = usuario.email
        es_corporativo = correo_usuario.lower().endswith("@fpatrimonionatural.org.co") if correo_usuario else False
        es_invitado_por_dominio = not es_corporativo

        if usuario.is_guest and es_corporativo:
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "No se permiten correos asociados a la fundación para usuarios invitados"
            return respuesta

        # Validar duplicados por correo e identificación
        if validar_usuario_existente(usuario.email, db, usuario.identification_number):
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "Ya existe un usuario registrado con este correo o documento de identificación"
            return respuesta

        # Doble verificación inmediatamente antes de insertar 
        if not validar_usuario_existente(usuario.email, db, usuario.identification_number):

            if usuario.is_guest or es_invitado_por_dominio:
                usuario_entra = obtener_usuario_entra_por_correo(correo_usuario)
                if not usuario_entra:
                    respuestaUsuarioInvitado = crear_usuario_invitado_AD(usuario)
                else:
                    respuestaUsuarioInvitado = reenviar_invitacion_usuario_AD(usuario)
                    usuario.guid_msft = usuario_entra.get("id")

                if not respuestaUsuarioInvitado["registro_exitoso"]:
                    respuesta.solicitud_exitosa = False
                    respuesta.mensaje = respuestaUsuarioInvitado["mensaje"]
                    return respuesta
                else:
                    if not usuario.guid_msft:
                        usuario.guid_msft = respuestaUsuarioInvitado["user_id"]
                    logging.info(f"Usuario invitado gestionado en AD con ID: {usuario.guid_msft}")

            raw_password = "AccesoSiva*.202"
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')
            hashed_password = hashed_password.replace('$2b$', '$2y$', 1)

            new_usuario = Users(
                guid_msft=usuario.guid_msft if usuario.guid_msft else None,
                first_name=usuario.first_name,
                last_name=usuario.last_name,
                other_name=usuario.other_name if usuario.other_name else None,
                other_last_name=usuario.other_last_name if usuario.other_last_name else None,
                email=usuario.email,
                position=usuario.position if usuario.position != -1 else None,
                identification_type=usuario.identification_type if usuario.identification_type else None,
                identification_number=usuario.identification_number if usuario.identification_number != -1 else None,
                is_active=usuario.is_active,
                is_guest=usuario.is_guest,
                password=hashed_password
            )
            db.add(new_usuario)
            
            try:
                db.commit()
                db.refresh(new_usuario)
            except Exception as commit_error:
                db.rollback()
                # Capturar errores de constraint único
                error_msg = str(commit_error).lower()
                if 'unique' in error_msg or 'duplicate' in error_msg:
                    if 'correo' in error_msg or 'email' in error_msg:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "Ya existe un usuario con este correo electrónico"
                    elif 'identificacion' in error_msg:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "Ya existe un usuario con este número de identificación"
                    else:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "El usuario ya está registrado"
                    logging.warning(f"Intento de crear usuario duplicado: {error_msg}")
                    return respuesta
                else:
                    raise  # Re-lanzar si no es error de duplicado
            

            model_type = UsuariosRepository.obtener_model_type_por_usuario(int(new_usuario.id), db)
            UsuariosRepository.reemplazar_programas_usuario(int(new_usuario.id), usuario.program_ids or [], db)
            UsuariosRepository.reemplazar_roles_usuario(int(new_usuario.id), usuario.role_ids or [], model_type, db)
            
            try:
                db.commit()
                db.refresh(new_usuario)
            except Exception as commit_error:
                db.rollback()
                # Capturar errores de constraint único
                error_msg = str(commit_error).lower()
                if 'unique' in error_msg or 'duplicate' in error_msg:
                    if 'correo' in error_msg or 'email' in error_msg:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "Ya existe un usuario con este correo electrónico"
                    elif 'identificacion' in error_msg:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "Ya existe un usuario con este número de identificación"
                    else:
                        respuesta.solicitud_exitosa = False
                        respuesta.mensaje = "El usuario ya está registrado"
                    logging.warning(f"Intento de crear usuario duplicado: {error_msg}")
                    return respuesta
                else:
                    raise  # Re-lanzar si no es error de duplicado
            
            logging.info(f"Created new usuario uuid: {new_usuario.guid}")
            respuesta.mensaje = "Usuario creado exitosamente"
            respuesta.identity = new_usuario.id
            respuesta.guid = str(new_usuario.guid)
            return respuesta
        else:
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "El correo ya se encuentra registrado"
            return respuesta
        
    except Exception as e:
        respuesta.solicitud_exitosa = False
        respuesta.mensaje = str(e)
        logging.error(f"Failed to create usuario: {str(e)}")
        return respuesta
        # raise PruebaCreationError(str(e))



def validar_usuario_existente(correo: str, db: Session, identificacion: str = None) -> bool:
    try:
        # Verificar por correo
        if correo:
            usuario = UsuariosRepository.obtener_por_correo(correo, db)
            if usuario:
                logging.info(f"Usuario with correo {correo} already exists")
                return True
        
        # Verificar por identificación si se proporciona
        if identificacion:
            usuario_por_doc = UsuariosRepository.obtener_por_identificacion(identificacion, db)
            if usuario_por_doc:
                logging.info(f"Usuario with identificacion {identificacion} already exists")
                return True
        
        return False
    except Exception as e:
        logging.error(f"Failed to validate existing usuario: {str(e)}")
        raise PruebaNotFoundError(str(e))

def cuerpo_correo_invitados() -> str:
    url_sistema = os.getenv("url_sistema")
    return f"""
            Estimado consultor,\n\n

            Le damos la bienvenida a Patrimonio Natural \n\n.

            Por medio de este correo le indicamos las instrucciones de acceso a la plataforma de gestión donde usted tramitará sus cuentas de cobro, informes mensuales de actividades y avances de productos. También podrá tramitar solicitudes de viaje para cumplir con compromisos contractuales si así lo requieren.\n\n

            Si requiere apoyo escribir a: siva@patrimonionatural.org.co \n\n

            NO responder a este correo ya que es un mensaje automático.
            """


def reenviar_invitacion_usuario_AD(usuario: UsuariosCreateBase) -> InvitacionResponse:
    email = usuario.email

    try:
        url_sistema = os.getenv("url_sistema")
        access_token = get_access_token()
        url = "https://graph.microsoft.com/v1.0/invitations"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "invitedUserEmailAddress": email,
            "inviteRedirectUrl": f"{url_sistema}login",
            "sendInvitationMessage": True,
            "invitedUserDisplayName": f"{usuario.first_name} {usuario.other_name} {usuario.last_name} {usuario.other_last_name}".strip(),
            "invitedUserMessageInfo": {
                "customizedMessageBody": cuerpo_correo_invitados(),
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code not in (200, 201):
            return {
                "registro_exitoso": False,
                "user_id": None,
                "mensaje": response.text
            }

        user = response.json()
        user_id = user.get("invitedUser", {}).get("id")

        return {
            "registro_exitoso": True,
            "user_id": user_id,
            "mensaje": "Invitación reenviada exitosamente"
        }

    except Exception as e:
        return {
            "registro_exitoso": False,
            "user_id": None,
            "mensaje": str(e)
        }
    

def crear_usuario_invitado_AD(usuario: UsuariosCreateBase) -> InvitacionResponse:
    # group_id = "55492ef4-3010-4554-90c0-46c2ebcc911f"
    email = usuario.email

    try:
        url_sistema = os.getenv("url_sistema")
        access_token = get_access_token()
        url = "https://graph.microsoft.com/v1.0/invitations"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "invitedUserEmailAddress": email,
            "inviteRedirectUrl": f"{url_sistema}/login",
            "sendInvitationMessage": True,
            "invitedUserDisplayName": f"{usuario.first_name} {usuario.other_name} {usuario.last_name} {usuario.other_last_name}".strip(),
            "invitedUserMessageInfo": {
                "customizedMessageBody": cuerpo_correo_invitados(),
                "ccRecipients": [
                    {
                        "emailAddress": {
                            "address": "siva@patrimonionatural.org.co"
                        }
                    }
                ]
                
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code not in (200, 201):
            return {
                "registro_exitoso": False,
                "user_id": None,
                "mensaje": response.text
            }

        user = response.json()
        user_id = user["invitedUser"]["id"]
        

        return {
            "registro_exitoso": True,
            "user_id": user_id,
            "mensaje": "Usuario invitado creado exitosamente"
        }

    except Exception as e:
        return {
            "registro_exitoso": False,
            "user_id": None,
            "mensaje": str(e)
        }


def validar_usuario_corporativo(guid: str, guid_msft: str, nombre: str = None, correo: str = None, db: Session = None) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario_db = UsuariosRepository.obtener_por_guid(guid, db)
        if not usuario_db:
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "Usuario no encontrado"
            return respuesta

        # Validar dominio del correo si se proporciona
        es_corporativo = correo.lower().endswith("@patrimonionatural.org.co") if correo else True
        es_invitado_por_dominio = not es_corporativo
        
        # Si es usuario invitado (dominio no corporativo), validar/crear en Entra
        # if es_invitado_por_dominio and correo:
        #     usuario_entra = obtener_usuario_entra_por_correo(correo)
            
        #     if not usuario_entra:
        #         # Usuario no existe en Entra, crear invitación
        #         usuario_temp = UsuariosCreateBase(
        #             email=correo,
        #             full_name=nombre or usuario_db.first_name
        #         )
        #         respuesta_invitacion = crear_usuario_invitado_AD(usuario_temp)
        #         if not respuesta_invitacion["registro_exitoso"]:
        #             respuesta.solicitud_exitosa = False
        #             respuesta.mensaje = respuesta_invitacion["mensaje"]
                    
        #         guid_msft = respuesta_invitacion["user_id"]
        #         logging.info(f"Usuario invitado creado en AD con ID: {guid_msft}")
        #     else:
        #         # Usuario existe en Entra, reenviar invitación
        #         usuario_temp = UsuariosCreateBase(
        #             correo=correo,
        #             nombre=nombre or usuario_db.nombre,
        #             telefono=usuario_db.telefono or "",
        #             correo_personal=correo,
        #             es_invitado=True
        #         )
        #         respuesta_invitacion = reenviar_invitacion_usuario_AD(usuario_temp)
        #         if not respuesta_invitacion["registro_exitoso"]:
        #             respuesta.solicitud_exitosa = False
        #             respuesta.mensaje = respuesta_invitacion["mensaje"]
        #             # return respuesta
        #         guid_msft = usuario_entra.get("id")
        #         logging.info(f"Invitación reenviada para usuario: {correo}")

        #     usuario_db.correo_corporativo_validado = True
        #     usuario_db.guid_msft = respuesta_invitacion["user_id"]
        #     usuario_db.nombre = nombre or usuario_db.nombre
        #     usuario_db.correo = correo
        #     db.commit()
        #     return respuesta
            
        # Actualizar guid_msft
        if guid_msft:
            usuario_db.guid_msft = guid_msft
        
        # Actualizar nombre si se proporciona
        # if nombre:
        #     usuario_db.nombre = nombre
        
        # # Actualizar correo si se proporciona
        # if correo:
        #     usuario_db.correo = correo
        
        # Marcar como validado
        # usuario_db.correo_corporativo_validado = True
        
        db.commit()
        db.refresh(usuario_db)

        respuesta.mensaje = "Usuario validado correctamente"
        logging.info(f"Usuario validado: {usuario_db.guid}, guid_msft: {guid_msft}")
        return respuesta
    except Exception as e:
        respuesta.solicitud_exitosa = False
        respuesta.mensaje = str(e)
        logging.error(f"Failed to validate usuario: {str(e)}")
        return respuesta


def obtener_usuario_para_edicion(guid: str, db: Session) -> UsuariosEdicionBase | None:
    try:
        usuario = UsuariosRepository.obtener_por_guid(guid, db)
        if not usuario:
            return None

        programas = UsersProgramsRepository.listar_ids_programas_por_usuario(int(usuario.id), db)
        roles = UsuariosRepository.listar_roles_por_usuario(int(usuario.id), db)

        return UsuariosEdicionBase(
            guid=usuario.guid,
            first_name=usuario.first_name,
            last_name=usuario.last_name,
            identification_type=int(usuario.identification_type),
            identification_number=int(usuario.identification_number),
            email=usuario.email,
            is_active=bool(usuario.is_active),
            other_name=usuario.other_name,
            other_last_name=usuario.other_last_name,
            position=usuario.position,
            program_ids=programas,
            role_ids=roles,
        )
    except Exception as e:
        logging.error(f"Failed to get usuario para edicion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def actualizar_usuario(guid: str, payload: UsuariosUpdateBase, db: Session) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=False)

    try:
        usuario = UsuariosRepository.obtener_por_guid(guid, db)
        if not usuario:
            respuesta.mensaje = 'Usuario no encontrado'
            return respuesta

        usuario.first_name = (payload.first_name or '').strip()
        usuario.last_name = (payload.last_name or '').strip()
        usuario.other_name = (payload.other_name or '').strip() or None
        usuario.other_last_name = (payload.other_last_name or '').strip() or None
        usuario.email = (payload.email or '').strip()
        usuario.position = (payload.position or '').strip() or None
        usuario.identification_type = int(payload.identification_type)
        usuario.identification_number = int(payload.identification_number)
        usuario.is_active = bool(payload.is_active)

        model_type = UsuariosRepository.obtener_model_type_por_usuario(int(usuario.id), db)
        UsuariosRepository.reemplazar_programas_usuario(int(usuario.id), payload.program_ids or [], db)
        UsuariosRepository.reemplazar_roles_usuario(int(usuario.id), payload.role_ids or [], model_type, db)
        UsuariosRepository.guardar(db)


        correo_usuario = usuario.email
        es_corporativo = correo_usuario.lower().endswith("@fpatrimonionatural.org.co") if correo_usuario else False
        es_invitado_por_dominio = not es_corporativo

        if (usuario.is_guest or es_invitado_por_dominio) and payload.reenviar_invitacion:
            usuario_entra = obtener_usuario_entra_por_correo(correo_usuario)
            if not usuario_entra:
                respuestaUsuarioInvitado = crear_usuario_invitado_AD(usuario)
            else:
                respuestaUsuarioInvitado = reenviar_invitacion_usuario_AD(usuario)
                usuario.guid_msft = usuario_entra.get("id")

            if not respuestaUsuarioInvitado["registro_exitoso"]:
                respuesta.solicitud_exitosa = False
                respuesta.mensaje = respuestaUsuarioInvitado["mensaje"]
                return respuesta
            else:
                if not usuario.guid_msft:
                    usuario.guid_msft = respuestaUsuarioInvitado["user_id"]
                logging.info(f"Usuario invitado gestionado en AD con ID: {usuario.guid_msft}")
                
        respuesta.solicitud_exitosa = True
        respuesta.mensaje = 'Usuario actualizado correctamente'
        return respuesta
    except Exception as e:
        db.rollback()
        respuesta.solicitud_exitosa = False
        respuesta.mensaje = str(e)
        logging.error(f"Failed to update usuario: {str(e)}")
        return respuesta
    