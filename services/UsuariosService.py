import os
from fastapi import HTTPException

from sqlalchemy.orm import Session
from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from exceptions import PruebaCreationError, PruebaNotFoundError
import logging
from dto.UsuariosDTO import (
    UsuariosBase,
    UsuariosCreateBase,
    UsuariosEdicionBase,
    UsuariosUpdateBase,
)
from repository import UsuariosRepository
from dto.ResponseRequest import ResponseRequest
from pathlib import Path
import json
import msal
import requests
from typing import List, Optional, TypedDict


class InvitacionResponse(TypedDict):
    registro_exitoso: bool
    user_id: Optional[str]
    mensaje: str


SCOPE = ["https://graph.microsoft.com/.default"]


def agregar_usuario_a_grupo(guid: str, access_token: str):
    group_id = (os.getenv("grupo_usuarios") or "").strip()

    if not group_id:
        raise HTTPException(
            status_code=500, detail="La variable grupo_usuarios no esta configurada"
        )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    check_membership_url = (
        f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/{guid}"
    )
    membership_response = requests.get(check_membership_url, headers=headers)

    if membership_response.status_code == 200:
        return {
            "agregado": False,
            "guid_msft": guid,
            "mensaje": "El usuario ya pertenece al grupo corporativo",
        }

    if membership_response.status_code != 404:
        raise HTTPException(
            status_code=membership_response.status_code, detail=membership_response.text
        )

    add_member_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
    payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{guid}"}
    add_response = requests.post(add_member_url, headers=headers, json=payload)

    if add_response.status_code in (200, 204):
        return {
            "agregado": True,
            "guid_msft": guid,
            "mensaje": "Usuario agregado correctamente al grupo corporativo",
        }

    if add_response.status_code == 400:
        raise HTTPException(
            status_code=400,
            detail="No fue posible agregar el usuario al grupo. Verifique que el guid exista en Azure AD y sea un directory object valido.",
        )

    raise HTTPException(status_code=add_response.status_code, detail=add_response.text)


def listar_usuarios(db: Session) -> list[UsuariosBase]:
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
                full_name=f"{usuario.first_name} {usuario.other_name or ''} {usuario.last_name} {usuario.other_last_name or ''}".strip(),
            )
            for usuario in usuarios
        ]
        return usuarios_dtos
    except Exception as e:
        logging.error(f"Failed to list usuarios: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_msal_app():
    file = Path("settings.json").absolute()
    if not file.exists():
        raise Exception(
            "settings.json file not found, please see settings_template.json"
        )
    with open(file) as fin:
        settings = json.load(fin)
        return msal.ConfidentialClientApplication(
            settings.get("client_id"),
            authority=f"https://login.microsoftonline.com/{settings.get('tenant_id')}",
            client_credential=settings.get("client_secret"),
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
            "Content-Type": "application/json",
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


def validar_usuario_corporativo(
    guid: str,
    guid_msft: str,
    nombre: str = None,
    correo: str = None,
    db: Session = None,
) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario_db = UsuariosRepository.obtener_por_guid(guid, db)
        if not usuario_db:
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "Usuario no encontrado"
            return respuesta

        # Validar dominio del correo si se proporciona
        es_corporativo = (
            correo.lower().endswith("@patrimonionatural.org.co") if correo else True
        )
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

        programas = UsuariosRepository.listar_programas_por_usuario(int(usuario.id), db)
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


def actualizar_usuario(
    guid: str, payload: UsuariosUpdateBase, db: Session
) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=False)

    try:
        usuario = UsuariosRepository.obtener_por_guid(guid, db)
        if not usuario:
            respuesta.mensaje = "Usuario no encontrado"
            return respuesta

        usuario.first_name = (payload.first_name or "").strip()
        usuario.last_name = (payload.last_name or "").strip()
        usuario.other_name = (payload.other_name or "").strip() or None
        usuario.other_last_name = (payload.other_last_name or "").strip() or None
        usuario.email = (payload.email or "").strip()
        usuario.position = (payload.position or "").strip() or None
        usuario.identification_type = int(payload.identification_type)
        usuario.identification_number = int(payload.identification_number)
        usuario.is_active = bool(payload.is_active)

        model_type = UsuariosRepository.obtener_model_type_por_usuario(
            int(usuario.id), db
        )
        UsuariosRepository.reemplazar_programas_usuario(
            int(usuario.id), payload.program_ids or [], db
        )
        UsuariosRepository.reemplazar_roles_usuario(
            int(usuario.id), payload.role_ids or [], model_type, db
        )
        UsuariosRepository.guardar(db)

        respuesta.solicitud_exitosa = True
        respuesta.mensaje = "Usuario actualizado correctamente"
        return respuesta
    except Exception as e:
        db.rollback()
        respuesta.solicitud_exitosa = False
        respuesta.mensaje = str(e)
        logging.error(f"Failed to update usuario: {str(e)}")
        return respuesta
