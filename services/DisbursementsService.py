from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from dto.DisbursementsDTO import DesembolsoDTO
from entity.agreements import Agreements
from entity.disbursement import Disbursement
from entity.disbursement_products import DisbursementProducts
from entity.disbursement_state import DisbursementState
from repository import AgreementsProductsRepository


def listar_estados(db: Session) -> list[dict]:
    return [{"id": estado.id, "name": estado.name}
            for estado in db.scalars(select(DisbursementState).order_by(DisbursementState.id))]


def obtener_desembolsos(id_agreement: int, db: Session) -> list[dict]:
    filas = AgreementsProductsRepository.obtener_desembolsos_por_id_agreement(id_agreement, db)
    resultado = {}
    for desembolso, producto in filas:
        if desembolso.id not in resultado:
            resultado[desembolso.id] = {
                campo: getattr(desembolso, campo) for campo in (
                    "id", "number_disbursement", "scheduled_date", "value", "state_id",
                    "request_date", "validation_date", "approval_date", "disbursement_date",
                    "documento_soporte", "observations",
                )
            }
            resultado[desembolso.id]["product_keys"] = []
        key = f"id:{producto.id}"
        if key not in resultado[desembolso.id]["product_keys"]:
            resultado[desembolso.id]["product_keys"].append(key)
    return list(resultado.values())


def guardar_desembolsos(
    id_agreement: int, desembolsos: list[DesembolsoDTO],
    productos_nuevos: dict[str, int], db: Session,
) -> None:
    db.execute(select(Agreements.id).where(
        Agreements.id == id_agreement
    ).with_for_update()).scalar_one()
    existentes = {d["id"]: d for d in obtener_desembolsos(id_agreement, db)}
    registros = {
        p.id: p for p in AgreementsProductsRepository.obtener_por_id_agreement(id_agreement, db)
    }
    productos_validos = set()
    for producto in registros.values():
        actividad = registros.get(producto.id_product)
        objetivo = registros.get(actividad.id_product) if actividad else None
        if objetivo and not objetivo.id_product:
            productos_validos.add(producto.id)
    asociaciones = list(db.scalars(select(DisbursementProducts).where(
        DisbursementProducts.product_id.in_(productos_validos)
    )))
    usados: dict[int, set[int]] = {}
    for enlace in asociaciones:
        usados.setdefault(enlace.product_id, set()).add(enlace.disbursement_id)
    editados = {entrada.id for entrada in desembolsos
                if entrada.id in existentes and entrada.model_fields_set != {"id"}}
    for propietarios in usados.values():
        propietarios.difference_update(editados)
    estados = {e["id"] for e in listar_estados(db)}
    procesados = set()

    for entrada in desembolsos:
        if entrada.id is not None:
            if entrada.id not in existentes:
                raise ValueError("El desembolso no pertenece al acuerdo")
            if entrada.id in procesados:
                raise ValueError("No se puede repetir un desembolso en la solicitud")
            procesados.add(entrada.id)
            if entrada.model_fields_set == {"id"}:
                continue
        estado = (existentes[entrada.id]["state_id"]
                  if entrada.id is not None and "state_id" not in entrada.model_fields_set
                  else entrada.state_id or 1)
        if (entrada.id is None or "state_id" in entrada.model_fields_set) and estado not in estados:
            raise ValueError("El estado del desembolso no existe")
        ids = []
        claves = (existentes[entrada.id]["product_keys"]
                  if entrada.id is not None and "product_keys" not in entrada.model_fields_set
                  else entrada.product_keys)
        for key in claves:
            if key.startswith("id:") and key[3:].isdigit():
                identity = int(key[3:])
            else:
                identity = productos_nuevos.get(key)
            if identity not in productos_validos:
                raise ValueError("El producto no pertenece al acuerdo o no es de nivel producto")
            if usados.get(identity):
                raise ValueError("El producto ya esta asociado a un desembolso")
            ids.append(identity)
        datos = entrada.model_dump(
            exclude={"id", "product_keys", "state_id"}, exclude_unset=entrada.id is not None
        )
        if entrada.id is None:
            desembolso = Disbursement(
                **datos, state_id=estado, created_at=datetime.now(), updated_at=datetime.now()
            )
            db.add(desembolso)
            enlaces = []
        else:
            desembolso = db.get(Disbursement, entrada.id)
            if desembolso is None:
                raise ValueError("El desembolso no existe")
            enlaces = list(db.scalars(select(DisbursementProducts).where(
                DisbursementProducts.disbursement_id == entrada.id
            )))
            if any(enlace.product_id not in productos_validos for enlace in enlaces):
                raise ValueError("El desembolso contiene productos ajenos al acuerdo")
            for campo, valor in datos.items():
                setattr(desembolso, campo, valor)
            desembolso.state_id = estado
            desembolso.updated_at = datetime.now()
        db.flush()
        actuales = {enlace.product_id for enlace in enlaces}
        for enlace in enlaces:
            if enlace.product_id not in ids:
                db.delete(enlace)
                usados[enlace.product_id].discard(desembolso.id)
        for identity in set(ids) - actuales:
            db.add(DisbursementProducts(disbursement_id=desembolso.id, product_id=identity))
        for identity in ids:
            usados.setdefault(identity, set()).add(desembolso.id)
    db.flush()
