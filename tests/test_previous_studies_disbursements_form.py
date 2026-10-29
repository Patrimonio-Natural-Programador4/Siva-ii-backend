import os
import unittest
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "sqlite://")

import api
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import Column, Integer, MetaData, Table, create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from dto.AgreementsProductsDTO import ObjetivoDTO
from dto.DisbursementsDTO import DesembolsoDTO
from entity.agreements_products import AgreementsProducts
from entity.disbursement import Disbursement
from entity.disbursement_products import DisbursementProducts
from entity.disbursement_state import DisbursementState
from services import AgreementsProductsService as products
from services import DisbursementsService as service
from services import PreviousStudiesService as studies
from controllers.PreviousStudiesController import router
from database.database import get_db
from dependencies.auth_dependency import get_current_user_oid
from dto.PreviousStudiesDTO import PreviousStudiesBase


class DisbursementsFormTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        metadata = MetaData()
        Table("agreements", metadata, Column("id", Integer, primary_key=True))
        for model in (AgreementsProducts, Disbursement, DisbursementProducts, DisbursementState):
            tabla = model.__table__.to_metadata(metadata)
            tabla.c.id.type = Integer()
        metadata.create_all(self.engine)
        self.db = Session(self.engine)
        self.addCleanup(self.engine.dispose)
        self.addCleanup(self.db.close)
        self.db.execute(metadata.tables["agreements"].insert(), [{"id": 7}, {"id": 8}])
        self.db.add(DisbursementState(id=1, name="Programado"))
        objetivo = ObjetivoDTO.model_validate({
            "product": "Objetivo", "actividades": [{
                "code": "1.1", "product": "Actividad", "productos": [{
                    "client_id": "producto-temporal", "code": "P1", "product": "Producto",
                    "unit_measure": "Informe", "quantity": 1,
                }],
            }],
        })
        self.mapa = products.guardar_objetivos(7, [objetivo], self.db)
        self.db.commit()
        self.data = {
            "number_disbursement": 1, "scheduled_date": "2026-11-01",
            "value": "1200.50", "product_keys": ["new:producto-temporal"],
            "state_id": 1, "request_date": "2026-10-27",
            "documento_soporte": "Referencia", "observations": "Observacion",
        }

    def test_guarda_y_recupera_desembolso_con_producto_nuevo(self):
        service.guardar_desembolsos(7, [DesembolsoDTO(**self.data)], self.mapa, self.db)
        self.db.commit()
        resultado = service.obtener_desembolsos(7, self.db)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["value"], Decimal("1200.50"))
        self.assertEqual(resultado[0]["scheduled_date"], date(2026, 11, 1))
        self.assertEqual(resultado[0]["state_id"], 1)
        self.assertEqual(resultado[0]["documento_soporte"], "Referencia")
        self.assertEqual(len(resultado[0]["product_keys"]), 1)
        service.guardar_desembolsos(7, [DesembolsoDTO(**resultado[0])], {}, self.db)
        self.db.commit()
        self.assertEqual(len(self.db.scalars(select(Disbursement)).all()), 1)

    def test_rechaza_producto_ya_asociado(self):
        service.guardar_desembolsos(7, [DesembolsoDTO(**self.data)], self.mapa, self.db)
        self.db.commit()
        with self.assertRaisesRegex(ValueError, "asociado"):
            service.guardar_desembolsos(7, [DesembolsoDTO(**self.data)], self.mapa, self.db)
        self.db.rollback()
        self.assertEqual(len(self.db.scalars(select(Disbursement)).all()), 1)

    def test_edita_datos_y_productos_conservando_identidad(self):
        service.guardar_desembolsos(7, [DesembolsoDTO(**self.data)], self.mapa, self.db)
        self.db.commit()
        original = service.obtener_desembolsos(7, self.db)[0]
        creado = self.db.get(Disbursement, original["id"]).created_at
        producto = self.db.get(AgreementsProducts, self.mapa["new:producto-temporal"])
        nuevo = AgreementsProducts(
            id_agreement=7, id_product=producto.id_product, code="P2", product="Nuevo"
        )
        self.db.add(nuevo)
        self.db.commit()
        cambio = {**original, "value": "2300.75", "observations": "Editado",
                  "product_keys": [f"id:{nuevo.id}"], "request_date": ""}
        service.guardar_desembolsos(7, [DesembolsoDTO(**cambio)], {}, self.db)
        self.db.commit()
        self.db.expire_all()
        resultado = service.obtener_desembolsos(7, self.db)[0]
        self.assertEqual(resultado["id"], original["id"])
        self.assertEqual(resultado["value"], Decimal("2300.75"))
        self.assertEqual(resultado["observations"], "Editado")
        self.assertIsNone(resultado["request_date"])
        self.assertEqual(resultado["product_keys"], [f"id:{nuevo.id}"])
        self.assertEqual(self.db.get(Disbursement, original["id"]).created_at, creado)
        self.assertEqual(len(self.db.scalars(select(DisbursementProducts)).all()), 1)
        service.guardar_desembolsos(7, [DesembolsoDTO(id=original["id"])], {}, self.db)
        self.db.commit()
        self.assertEqual(service.obtener_desembolsos(7, self.db)[0]["value"], Decimal("2300.75"))

    def test_edicion_rechaza_productos_ocupados_y_revierte(self):
        service.guardar_desembolsos(7, [DesembolsoDTO(**self.data)], self.mapa, self.db)
        producto = self.db.get(AgreementsProducts, self.mapa["new:producto-temporal"])
        otro = AgreementsProducts(id_agreement=7, id_product=producto.id_product, code="P2", product="Otro")
        self.db.add(otro)
        self.db.flush()
        service.guardar_desembolsos(7, [DesembolsoDTO(**{
            **self.data, "number_disbursement": 2, "product_keys": [f"id:{otro.id}"],
        })], {}, self.db)
        self.db.commit()
        registros = service.obtener_desembolsos(7, self.db)
        with self.assertRaisesRegex(ValueError, "asociado"):
            service.guardar_desembolsos(7, [DesembolsoDTO(**{
                **registros[0], "product_keys": registros[1]["product_keys"], "value": "500",
            })], {}, self.db)
        self.db.rollback()
        self.assertEqual(service.obtener_desembolsos(7, self.db), registros)
        # A final-state swap must not depend on the ordering of entries.
        service.guardar_desembolsos(7, [
            DesembolsoDTO(**{**registros[0], "product_keys": registros[1]["product_keys"]}),
            DesembolsoDTO(**{**registros[1], "product_keys": registros[0]["product_keys"]}),
        ], {}, self.db)
        self.db.commit()
        resultado = {d["id"]: d for d in service.obtener_desembolsos(7, self.db)}
        self.assertEqual(resultado[registros[0]["id"]]["product_keys"], registros[1]["product_keys"])

    def test_rechaza_producto_ajeno_objetivo_y_referencia_desconocida(self):
        objetivo = self.db.scalars(select(AgreementsProducts).where(
            AgreementsProducts.id_product.is_(None)
        )).one()
        for acuerdo, key in [(8, f"id:{self.mapa['new:producto-temporal']}"),
                             (7, f"id:{objetivo.id}"), (7, "new:inexistente")]:
            with self.subTest(acuerdo=acuerdo, key=key), self.assertRaises(ValueError):
                service.guardar_desembolsos(
                    acuerdo, [DesembolsoDTO(**{**self.data, "product_keys": [key]})], {}, self.db
                )
            self.db.rollback()

    def test_valida_requeridos_y_precision(self):
        for cambio in [
            {"product_keys": []}, {"value": -1}, {"value": "1.001"},
            {"number_disbursement": 0}, {"number_disbursement": 1.5},
            {"scheduled_date": "no-fecha"},
            {"product_keys": ["id:1", "id:1"]},
        ]:
            with self.subTest(cambio=cambio), self.assertRaises(ValidationError):
                DesembolsoDTO(**{**self.data, **cambio})

    def test_rechaza_estado_inexistente_y_desembolso_ajeno(self):
        for cambio in [{"state_id": 999}, {"id": 999}]:
            with self.subTest(cambio=cambio), self.assertRaises(ValueError):
                service.guardar_desembolsos(
                    7, [DesembolsoDTO(**{**self.data, **cambio})], self.mapa, self.db
                )
            self.db.rollback()

    def test_error_revierte_todo_el_lote(self):
        with self.assertRaises(ValueError):
            service.guardar_desembolsos(7, [
                DesembolsoDTO(**self.data),
                DesembolsoDTO(**{**self.data, "number_disbursement": 2}),
            ], self.mapa, self.db)
        self.db.rollback()
        self.assertEqual(service.obtener_desembolsos(7, self.db), [])

    def test_api_guarda_producto_y_desembolso_en_una_sola_solicitud(self):
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_db] = lambda: self.db
        app.dependency_overrides[get_current_user_oid] = lambda: "usuario"
        registro = SimpleNamespace(**{campo: None for campo in PreviousStudiesBase.model_fields})
        registro.id = 12
        registro.code = "EP-PRUEBA"
        objetivo = {
            "product": "Otro objetivo", "actividades": [{
                "code": "2.1", "product": "Otra actividad", "productos": [{
                    "client_id": "otro", "code": "P2", "product": "Otro producto",
                    "unit_measure": "Informe", "quantity": 2,
                }],
            }],
        }
        with patch.object(studies.UsuariosRepository, "obtener_por_guid_msft", return_value=SimpleNamespace(id=1)), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_guid", return_value=registro), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_id", return_value=registro), \
                patch.object(studies.AgreementRepository, "obtener_por_id_estudio_previo",
                             return_value=SimpleNamespace(id=7)), \
                patch.object(self.db, "refresh"), TestClient(app) as client:
            guid = uuid4()
            catalogo = client.get("/estudios-previos/catalogos/estados-desembolso")
            self.assertEqual(catalogo.status_code, 200)
            self.assertEqual(catalogo.json(), [{"id": 1, "name": "Programado"}])
            response = client.put(f"/estudios-previos/{guid}", json={
                "objetivos": [objetivo],
                "desembolsos": [{**self.data, "product_keys": ["new:otro"]}],
            })
            self.assertEqual(response.status_code, 200, response.text)
            response = client.get(f"/estudios-previos/{guid}/detalle")
            self.assertEqual(response.status_code, 200, response.text)
            desembolsos = response.json()["desembolsos"]
            self.assertEqual(len(desembolsos), 1)
            self.assertEqual(desembolsos[0]["value"], "1200.50")
            identity = int(desembolsos[0]["product_keys"][0][3:])
            self.assertEqual(self.db.get(AgreementsProducts, identity).product, "Otro producto")
            # Reenviar un ID existente no cambia valores ni duplica asociaciones.
            response = client.put(f"/estudios-previos/{guid}", json={"desembolsos": desembolsos})
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(len(self.db.scalars(select(Disbursement)).all()), 1)
            desembolsos[0]["value"] = "9876.54"
            desembolsos[0]["observations"] = "Actualizado desde drawer"
            response = client.put(f"/estudios-previos/{guid}", json={"desembolsos": desembolsos})
            self.assertEqual(response.status_code, 200, response.text)
            response = client.get(f"/estudios-previos/{guid}/detalle")
            self.assertEqual(response.status_code, 200, response.text)
            actualizado = response.json()["desembolsos"][0]
            self.assertEqual(actualizado["id"], desembolsos[0]["id"])
            self.assertEqual(Decimal(actualizado["value"]), Decimal("9876.54"))
            self.assertEqual(actualizado["observations"], "Actualizado desde drawer")
            cantidad_productos = len(self.db.scalars(select(AgreementsProducts)).all())
            response = client.put(f"/estudios-previos/{guid}", json={
                "objetivos": [objetivo],
                "desembolsos": [{**self.data, "product_keys": [f"id:{identity}"]}],
            })
            self.assertEqual(response.status_code, 400, response.text)
            self.assertEqual(len(self.db.scalars(select(AgreementsProducts)).all()), cantidad_productos)
            self.assertEqual(len(self.db.scalars(select(Disbursement)).all()), 1)


if __name__ == "__main__":
    unittest.main()
