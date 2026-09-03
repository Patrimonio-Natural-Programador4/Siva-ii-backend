from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import status
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ResponseRequest import ResponseRequest
from dto.TermsReferenceDTO import TermsReferenceCreate
from services import TdrService, SolicitudesAprobacionService

router = APIRouter(
    prefix='/tdr',
    tags=['TDR']
)

@router.get("/listados")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return TdrService.lista_generica(db, user_oid)

@router.get("/campos_tdr")
def obtener_campos_tdr(approval_flow_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    campos_tdr = TdrService.obtener_campos_tdr(approval_flow_id, db)
    if not campos_tdr:
        raise HTTPException(status_code=404, detail="Campos TDR no encontrados")
    return campos_tdr

@router.post("", response_model=ResponseRequest)
def crear_tdr(tdr: TermsReferenceCreate, db: DbSession, background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = TdrService.crear_tdr(tdr, db, user_oid, background_tasks)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/previsualizar", response_model=ResponseRequest)
def previsualizar_tdr(tdr: TermsReferenceCreate, db: DbSession, background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = TdrService.previsualizar_tdr(tdr, db, user_oid, background_tasks)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))