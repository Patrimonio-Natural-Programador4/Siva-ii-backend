from datetime import datetime
import re

from sqlalchemy.orm import Session
from sqlalchemy import select

from dto.AgreementsProductsDTO import ObjetivoDTO
from entity.agreements_products import AgreementsProducts
from entity.agreements import Agreements
from repository.AgreementsProductsRepository import obtener_por_id_agreement as listar_registros


def obtener_objetivos(id_agreement: int, db: Session) -> list[dict]:
    registros = listar_registros(id_agreement, db)
    hijos: dict[int | None, list] = {}
    for registro in registros:
        hijos.setdefault(registro.id_product or None, []).append(registro)

    def orden(registro):
        return [
            (0, int(parte)) if parte.isdigit() else (1, parte.casefold())
            for parte in re.split(r"(\d+)", registro.code or "")
        ]

    def datos(registro):
        return {"id": registro.id, "code": registro.code, "product": registro.product}

    objetivos = []
    for objetivo in sorted(hijos.get(None, []), key=orden):
        actividades = []
        for actividad in sorted(hijos.get(objetivo.id, []), key=orden):
            productos = [{
                **datos(producto),
                "unit_measure": producto.unit_measure,
                "quantity": producto.quantity,
                "observations": producto.observations,
                "state_id": producto.state_id,
            } for producto in sorted(hijos.get(actividad.id, []), key=orden)]
            actividades.append({**datos(actividad), "productos": productos})
        objetivos.append({**datos(objetivo), "actividades": actividades})
    return objetivos


def guardar_objetivos(id_agreement: int, objetivos: list[ObjetivoDTO], db: Session) -> dict[str, int]:
    db.execute(
        select(Agreements.id).where(Agreements.id == id_agreement).with_for_update()
    ).scalar_one()
    registros = listar_registros(id_agreement, db)
    existentes = {registro.id: registro for registro in registros}
    usados: set[int] = set()
    referencias: set[str] = set()

    def validar(nodo, padre):
        if nodo.id is not None:
            registro = existentes.get(nodo.id)
            if registro is None or (registro.id_product or None) != padre or nodo.id in usados:
                raise ValueError("El registro no pertenece al acuerdo o a su padre")
            usados.add(nodo.id)

    def validar_productos(actividad):
        codigos = {
            registro.id: registro.code for registro in registros
            if actividad.id is not None and registro.id_product == actividad.id
        }
        for producto in actividad.productos:
            if producto.id is not None and producto.modificar:
                codigos[producto.id] = producto.code
        nuevos = set()
        for producto in actividad.productos:
            if producto.client_id:
                if producto.client_id in referencias:
                    raise ValueError("La referencia temporal del producto esta repetida")
                referencias.add(producto.client_id)
            validar(producto, actividad.id)
            if producto.id is None or producto.modificar:
                if producto.code in nuevos or producto.code in (
                    code for identity, code in codigos.items() if identity != producto.id
                ):
                    raise ValueError("El codigo del producto ya existe en esta actividad")
                if producto.id is None:
                    nuevos.add(producto.code)

    for objetivo in objetivos:
        validar(objetivo, None)
        for actividad in objetivo.actividades:
            if objetivo.id is None and actividad.id is not None:
                raise ValueError("Una actividad existente requiere su objetivo original")
            validar(actividad, objetivo.id)
            if actividad.id is None and any(p.id is not None for p in actividad.productos):
                raise ValueError("Un producto existente requiere su actividad original")
            validar_productos(actividad)

    siguiente = max((
        int(registro.code) for registro in registros
        if not registro.id_product and registro.code and registro.code.isdigit()
    ), default=0) + 1

    def insertar(nodo, padre, code, es_producto=False):
        if nodo.id is not None:
            if nodo.modificar:
                registro = existentes[nodo.id]
                registro.product = nodo.product
                if padre is not None:
                    registro.code = nodo.code
                if es_producto:
                    registro.unit_measure = nodo.unit_measure
                    registro.quantity = nodo.quantity
                    registro.observations = nodo.observations
            return nodo.id
        datos = {
            "id_agreement": id_agreement,
            "id_product": padre,
            "code": code,
            "product": nodo.product,
            "created_at": datetime.now(),
        }
        if es_producto:
            datos.update(
                unit_measure=nodo.unit_measure, quantity=nodo.quantity,
                observations=nodo.observations, state_id=1,
            )
        registro = AgreementsProducts(**datos)
        db.add(registro)
        db.flush()
        return registro.id

    productos_nuevos: dict[str, int] = {}
    for objetivo in objetivos:
        objetivo_id = insertar(objetivo, None, str(siguiente))
        if objetivo.id is None:
            siguiente += 1
        for actividad in objetivo.actividades:
            actividad_id = insertar(actividad, objetivo_id, actividad.code)
            for producto in actividad.productos:
                identity = insertar(producto, actividad_id, producto.code, es_producto=True)
                if producto.client_id:
                    productos_nuevos[f"new:{producto.client_id}"] = identity
    db.flush()
    return productos_nuevos
