import os
import json
import base64
import requests
import msal
import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def solicitud_viaje(titulo: str, to: list, body: str, cc: str = "", cco: str = "", db: Session = None):
    # --- 1. Obtener dirección de correo remitente ---
    FROM_EMAIL = os.getenv("FROM_EMAIL", "soportesiva@patrimonionatural.org.co")
    
    tenant_id = os.getenv("tenant_id")
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    if not tenant_id or not client_id or not client_secret:
        logger.error("Faltan variables de entorno para MSAL (tenant_id, client_id o client_secret).")
        return

    # --- 2. Obtener el token de acceso ---
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )
    result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

    if "access_token" not in result:
        logger.error(f"Error al obtener token de Graph: {result.get('error_description')}")
        return

    access_token = result['access_token']
    logger.info("Token de Microsoft Graph obtenido correctamente.")

    # --- 3. Preparar imagen del Logo si existe ---
    logo_base64 = ""
    logo_path = os.path.join('templates', 'logo_patrimonio.png')
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as ex:
            logger.error(f"Error al leer logo_patrimonio.png: {str(ex)}")

    # --- 4. Construir cuerpo del correo ---
    send_mail_url = f'https://graph.microsoft.com/v1.0/users/{FROM_EMAIL}/sendMail'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    attachments = []
    if logo_base64:
        attachments.append({
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": "logo_patrimonio.png",
            "contentBytes": logo_base64,
            "contentId": "logo",
            "isInline": True
        })

    email_message = {
        "message": {
            "subject": titulo,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": to,
            "attachments": attachments
        },
        "saveToSentItems": "true"
    }

    try:
        response = requests.post(send_mail_url, headers=headers, json=email_message)
        if response.status_code == 202:
            logger.info(f"Notificación de viaje '{titulo}' enviada exitosamente a: {to}")
        else:
            logger.error(f"Error de Graph al enviar correo: {response.status_code} - {response.text}")
    except Exception as ex:
        logger.error(f"Excepción al enviar correo por Graph API: {str(ex)}")
