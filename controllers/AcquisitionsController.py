from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from typing import Optional

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AcquisitionsDTO import AcquisitionsCreate
from dto.ResponseRequest import ResponseRequest
from services import AcquisitionsService


router = APIRouter(
    prefix='/adquisiciones',
    tags=['Adquisiciones']
)


@router.get('')
def list_acquisitions(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AcquisitionsService.list_acquisitions(db)


@router.get("/filtro")
def list_acquisitions_sp(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(1),
    filtro: str = Query(""),
    pid: Optional[int] = Query(-1),
    actividad: Optional[int] = Query(-1),
    procesos: Optional[list[str]] = Query(None),
    rubros: Optional[list[str]] = Query(None),
    rubros_cortos: Optional[list[str]] = Query(None),
    actividad_codigo: Optional[str] = Query(None),    
):
    try:
        return AcquisitionsService.list_acquisitions_sp(
            db, page, filtro, pid, actividad, procesos, rubros, rubros_cortos, actividad_codigo  
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{id}')
def get_acquisition_by_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    acquisition = AcquisitionsService.get_acquisition_by_id(id, db)
    if not acquisition:
        raise HTTPException(status_code=404, detail='Adquisición no encontrada')
    return acquisition


@router.post('', response_model=ResponseRequest)
def create_acquisition(payload: AcquisitionsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = AcquisitionsService.create_acquisition(payload, db, user_oid)
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=ResponseRequest)
def update_acquisition(id: int, payload: AcquisitionsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = AcquisitionsService.update_acquisition(id, payload, db, user_oid)
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id}', response_model=ResponseRequest)
def delete_acquisition(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = AcquisitionsService.delete_acquisition(id, db)
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))