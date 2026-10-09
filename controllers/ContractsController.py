from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from typing import Optional

from database.database import DbSession, get_db
from dependencies.auth_dependency import get_current_user_oid
from dto.ContractsDTO import ContractsBase, ContractsCreate, ContractListSP
from dto.ResponseRequest import ResponseRequest

from services import ContractsService


router = APIRouter(
    prefix='/contratos',
    tags=['Contratos']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ContractsService.listar(db)


@router.get("/filtro")
def listar_contracts_filtro(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    filtro: str = Query(""),
    anio: Optional[int] = Query(-1),
    tipo: Optional[int] = Query(-1),
    contrato_padre: Optional[int] = Query(-1),
):
    try:
        return ContractsService.listar_contracts_sp(
            db, page, filtro, anio, tipo, contrato_padre
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{id}')
def obtener_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    contrato = ContractsService.obtener_por_id(id, db)
    if not contrato:
        raise HTTPException(status_code=404, detail='Contrato no encontrado')
    return contrato


@router.post('', response_model=ResponseRequest)
def crear_contrato(payload: ContractsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = ContractsService.crear(payload, db, user_oid)
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        if response_request.solicitud_exitosa == False:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{id}', response_model=ResponseRequest)
def actualizar(id: int, payload: ContractsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        contrato_db = ContractsService.obtener_por_id(id, db)
        if not contrato_db:
            raise HTTPException(status_code=404, detail='Contrato no encontrado')
        response_request = ContractsService.actualizar(contrato_db.id, payload, db, user_oid)
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))