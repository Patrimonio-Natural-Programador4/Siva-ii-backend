import os
import jwt
from fastapi import Request, HTTPException, status
from jwt import PyJWKClient

# Configuración de Microsoft Entra sacada de .env / settings.json
TENANT_ID = os.getenv("tenant_id")
CLIENT_ID = os.getenv("client_id")
TOKEN_AUDIENCE = os.getenv("token_audience")
ALLOWED_AUDIENCES = os.getenv("allowed_audiences", "")

# URL donde Microsoft publica las llaves públicas para verificar firmas
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
jwks_client = PyJWKClient(JWKS_URL)


def _build_valid_audiences() -> list[str]:
    audiences: list[str] = []

    if TOKEN_AUDIENCE:
        audiences.append(TOKEN_AUDIENCE.strip())

    if CLIENT_ID:
        client_id = CLIENT_ID.strip()
        audiences.append(client_id)
        audiences.append(f"api://{client_id}")

    if ALLOWED_AUDIENCES:
        audiences.extend([aud.strip() for aud in ALLOWED_AUDIENCES.split(",") if aud.strip()])

    # Elimina duplicados conservando el orden.
    return list(dict.fromkeys(audiences))

def get_current_user_oid(request: Request) -> str:
    # Si un middleware/dependency previo ya validó el token, reutilizamos ese resultado
    # para evitar inconsistencias entre validadores distintos.
    claims = getattr(request.state, "user_claims", None)
    if isinstance(claims, dict):
        oid = claims.get("oid") or claims.get("sub")
        if oid:
            return oid

    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authorization header missing or invalid"
        )
    
    token = authorization_header.split(" ")[1]
    valid_audiences = _build_valid_audiences()

    if not valid_audiences:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No hay audiencias configuradas para validar el token"
        )

    try:
        # Obtener la llave pública específica que firmó este token
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Decodificar Y VALIDAR LA FIRMA del token
        # audience (aud) debe ser el client_id de esta aplicación
        valid_issuers = [
            f"https://sts.windows.net/{TENANT_ID}/",
            f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
        ]

        decoded = None
        last_error = None
        for issuer in valid_issuers:
            try:
                decoded = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience=valid_audiences,
                    issuer=issuer,
                )
                break
            except jwt.InvalidIssuerError as e:
                last_error = e

        if decoded is None:
            if last_error:
                raise last_error
            raise jwt.InvalidTokenError("No fue posible validar issuer del token")

        oid = decoded.get("oid") or decoded.get("sub")
        if not oid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token valido pero sin claims de identidad"
            )

        return oid

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Audience inválida. Audiencias permitidas: {', '.join(valid_audiences)}"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token inválido: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error de autenticación")