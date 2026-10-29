import os
import unittest
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Column, Integer, MetaData, Table, create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite://")

import api  # Registra los modelos relacionados igual que el arranque de la aplicacion.
from controllers.PreviousStudiesController import router
from database.database import get_db
from dependencies.auth_dependency import get_current_user_oid
from dto.AgreementsProductsDTO import ObjetivoDTO
from dto.PreviousStudiesDTO import PreviousStudiesBase
from entity.agreements_products import AgreementsProducts
from entity.disbursement import Disbursement
from entity.disbursement_products import DisbursementProducts
from services import AgreementsProductsService as products
from services import PreviousStudiesService as studies


class ProductsPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool,
        )
        metadata = MetaData()
        Table("agreements", metadata, Column("id", Integer, primary_key=True))
        tabla = AgreementsProducts.__table__.to_metadata(metadata)
        tabla.c.id.type = Integer()
        for model in (Disbursement, DisbursementProducts):
            tabla = model.__table__.to_metadata(metadata)
            tabla.c.id.type = Integer()
        metadata.create_all(self.engine)
        self.db = Session(self.engine)
        self.db.execute(metadata.tables["agreements"].insert().values(id=7))
        self.db.commit()
        self.addCleanup(self.engine.dispose)
        self.addCleanup(self.db.close)
        self.payload = {
            "product": "Objetivo de prueba",
            "actividades": [{
                "code": "1.1", "product": "Actividad de prueba",
                "productos": [{
                    "code": "P1", "product": "Producto de prueba",
                    "unit_measure": "Informes", "quantity": "2.50",
                    "observations": "Entrega parcial",
                }],
            }],
        }

    def test_persistencia_real_y_relectura_sin_duplicar_ids(self):
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(self.payload)], self.db)
        self.db.commit()
        leidos = products.obtener_objetivos(7, self.db)
        producto = leidos[0]["actividades"][0]["productos"][0]
        self.assertEqual(producto["state_id"], 1)
        self.assertEqual(producto["quantity"], Decimal("2.50"))
        self.assertEqual(producto["observations"], "Entrega parcial")
        ids = [r.id for r in self.db.scalars(select(AgreementsProducts))]
        self.db.get(AgreementsProducts, producto["id"]).state_id = 5
        self.db.commit()
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(leidos[0])], self.db)
        self.db.commit()
        self.assertEqual(ids, [r.id for r in self.db.scalars(select(AgreementsProducts))])
        self.assertEqual(self.db.get(AgreementsProducts, producto["id"]).state_id, 5)

    def test_agrega_hijos_a_registros_existentes_y_rechaza_codigos_repetidos(self):
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(self.payload)], self.db)
        self.db.commit()
        objetivo = ObjetivoDTO.model_validate(products.obtener_objetivos(7, self.db)[0])
        nuevo = objetivo.actividades[0].productos[0].model_copy(update={"id": None, "code": "P2"})
        objetivo.actividades[0].productos.append(nuevo)
        products.guardar_objetivos(7, [objetivo], self.db)
        self.db.commit()
        self.assertEqual(len(products.obtener_objetivos(7, self.db)[0]["actividades"][0]["productos"]), 2)
        with self.assertRaisesRegex(ValueError, "ya existe"):
            products.guardar_objetivos(7, [objetivo], self.db)
        self.db.rollback()
        self.assertEqual(len(self.db.scalars(select(AgreementsProducts)).all()), 4)

    def test_edita_objetivo_y_actividad_sin_cambiar_hijos_ni_estado(self):
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(self.payload)], self.db)
        self.db.commit()
        original = products.obtener_objetivos(7, self.db)[0]
        producto = original["actividades"][0]["productos"][0]
        self.db.get(AgreementsProducts, producto["id"]).state_id = 5
        self.db.commit()
        original.update(product="Objetivo editado", modificar=True)
        original["actividades"][0].update(code="A2", product="Actividad editada", modificar=True)
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(original)], self.db)
        self.db.commit()
        self.db.expire_all()
        resultado = products.obtener_objetivos(7, self.db)[0]
        self.assertEqual(resultado["id"], original["id"])
        self.assertEqual(resultado["code"], original["code"])
        self.assertEqual(resultado["product"], "Objetivo editado")
        actividad = resultado["actividades"][0]
        self.assertEqual(actividad["id"], original["actividades"][0]["id"])
        self.assertEqual(actividad["code"], "A2")
        self.assertEqual(actividad["product"], "Actividad editada")
        self.assertEqual(actividad["productos"][0], {**producto, "state_id": 5})
        self.assertEqual(len(self.db.scalars(select(AgreementsProducts)).all()), 3)

    def test_edita_producto_preserva_estado_y_rechaza_codigo_ocupado(self):
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(self.payload)], self.db)
        self.db.commit()
        original = products.obtener_objetivos(7, self.db)[0]
        producto = original["actividades"][0]["productos"][0]
        self.db.get(AgreementsProducts, producto["id"]).state_id = 5
        self.db.commit()
        producto.update(modificar=True, code="P2", product="Editado",
                        unit_measure="Documento", quantity="3.75", observations="Cambio")
        products.guardar_objetivos(7, [ObjetivoDTO.model_validate(original)], self.db)
        self.db.commit()
        self.db.expire_all()
        resultado = products.obtener_objetivos(7, self.db)[0]["actividades"][0]["productos"][0]
        self.assertEqual(resultado["id"], producto["id"])
        self.assertEqual(resultado["code"], "P2")
        self.assertEqual(resultado["product"], "Editado")
        self.assertEqual(resultado["unit_measure"], "Documento")
        self.assertEqual(resultado["quantity"], Decimal("3.75"))
        self.assertEqual(resultado["state_id"], 5)
        otro = {**producto, "id": None, "modificar": False}
        original["actividades"][0]["productos"].append(otro)
        with self.assertRaisesRegex(ValueError, "ya existe"):
            products.guardar_objetivos(7, [ObjetivoDTO.model_validate(original)], self.db)
        self.db.rollback()

    def test_rollback_no_deja_objetivos_huerfanos(self):
        original = self.db.flush
        llamadas = 0

        def fallar_en_producto(*args, **kwargs):
            nonlocal llamadas
            llamadas += 1
            if llamadas == 3:
                raise ValueError("Fallo de persistencia")
            return original(*args, **kwargs)

        with patch.object(self.db, "flush", side_effect=fallar_en_producto):
            with self.assertRaisesRegex(ValueError, "Fallo de persistencia"):
                products.guardar_objetivos(7, [ObjetivoDTO.model_validate(self.payload)], self.db)
        self.db.rollback()
        self.assertEqual(products.obtener_objetivos(7, self.db), [])

    def test_endpoint_actualizar_guarda_productos_y_valida_payload(self):
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_db] = lambda: self.db
        app.dependency_overrides[get_current_user_oid] = lambda: "usuario-prueba"
        registro = SimpleNamespace(**{campo: None for campo in PreviousStudiesBase.model_fields})
        registro.id = 12
        registro.code = "EP-PRUEBA"
        usuario = SimpleNamespace(id=3)
        guid = str(uuid4())
        with patch.object(studies.UsuariosRepository, "obtener_por_guid_msft", return_value=usuario), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_guid", return_value=registro), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_id", return_value=registro), \
                patch.object(studies.AgreementRepository, "obtener_por_id_estudio_previo",
                             return_value=SimpleNamespace(id=7)), \
                patch.object(self.db, "refresh"), TestClient(app) as client:
            response = client.put(f"/estudios-previos/{guid}", json={"objetivos": [self.payload]})
            self.assertEqual(response.status_code, 200, response.text)
            self.assertTrue(response.json()["solicitud_exitosa"])
            leidos = products.obtener_objetivos(7, self.db)
            self.assertEqual(leidos[0]["actividades"][0]["productos"][0]["code"], "P1")
            response = client.get(f"/estudios-previos/{guid}/detalle")
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(
                response.json()["objetivos"][0]["actividades"][0]["productos"][0]["quantity"], "2.50"
            )
            invalido = {**self.payload, "product": " "}
            response = client.put(f"/estudios-previos/{guid}", json={"objetivos": [invalido]})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(len(products.obtener_objetivos(7, self.db)), 1)

    def test_endpoint_rechaza_ids_ajenos_sin_insertar_registros(self):
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_db] = lambda: self.db
        app.dependency_overrides[get_current_user_oid] = lambda: "usuario-prueba"
        registro = SimpleNamespace(id=12)
        with patch.object(studies.UsuariosRepository, "obtener_por_guid_msft",
                          return_value=SimpleNamespace(id=3)), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_guid", return_value=registro), \
                patch.object(studies.PreviousStudiesRepository, "obtener_por_id", return_value=registro), \
                patch.object(studies.AgreementRepository, "obtener_por_id_estudio_previo",
                             return_value=SimpleNamespace(id=7)), TestClient(app) as client:
            response = client.put(
                f"/estudios-previos/{uuid4()}", json={"objetivos": [{**self.payload, "id": 999}]}
            )
        self.assertEqual(response.status_code, 400, response.text)
        self.assertFalse(response.json()["solicitud_exitosa"])
        self.assertEqual(products.obtener_objetivos(7, self.db), [])


if __name__ == "__main__":
    unittest.main()
