from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from dependencies.auth_dependency import get_current_user_oid
from services.WordParametersService import extraer_parametros


router = APIRouter(prefix="/documentos", tags=["Documentos"])


@router.post("/extraer-parametros")
async def extraer_parametros_documento(
    archivo: UploadFile = File(...),
    user_oid: str = Depends(get_current_user_oid),
):
    try:
        contenido = await archivo.read()
        parametros = extraer_parametros(archivo.filename or "", contenido)
        return {"parametros": parametros}
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    finally:
        await archivo.close()