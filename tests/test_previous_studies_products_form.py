import os
import unittest
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from fastapi import BackgroundTasks
from pydantic import ValidationError

os.environ.setdefault("DATABASE_URL", "sqlite://")

from dto.AgreementsProductsDTO import ObjetivoDTO, ProductoDTO
from dto.PreviousStudiesDTO import PreviousStudiesCreate
from dto.ResponseRequest import ResponseRequest
from services import AgreementsProductsService as service
from services import PreviousStudiesService as studies


class ProductsFormTests(unittest.TestCase):
    def objetivo(self, **changes):
        data = {
            "product": "Objetivo",
            "actividades": [{
                "code": "1.1",
                "product": "Actividad",
                "productos": [{
                    "code": "P1",
                    "product": "Producto",
                    "unit_measure": "Informes",
                    "quantity": "2.50",
                    "observations": "Entrega parcial",
                }],
            }],
        }
        data.update(changes)
        return ObjetivoDTO.model_validate(data)

    def test_valida_campos_y_precision(self):
        producto = self.objetivo().actividades[0].productos[0]
        self.assertEqual(producto.quantity, Decimal("2.50"))
        for campo, valor in [
            ("code", " "), ("product", ""), ("unit_measure", " "),
            ("quantity", -1), ("quantity", "1.001"), ("quantity", "NaN"),
        ]:
            data = producto.model_dump()
            data[campo] = valor
            with self.subTest(campo=campo, valor=valor), self.assertRaises(ValidationError):
                ProductoDTO.model_validate(data)

    def test_omitir_objetivos_no_equivale_a_borrarlos(self):
        self.assertIsNone(PreviousStudiesCreate().objetivos)
        self.assertEqual(PreviousStudiesCreate(objetivos=[]).objetivos, [])

    def test_inserta_tres_niveles_con_estado_inicial_y_codigo_automatico(self):
        db = Mock()
        creados = []

        def crear(**data):
            registro = SimpleNamespace(id=len(creados) + 10, **data)
            creados.append(registro)
            return registro

        existente = SimpleNamespace(id=1, id_product=None, code="9")
        with patch.object(service, "listar_registros", return_value=[existente]), \
                patch.object(service, "AgreementsProducts", side_effect=crear):
            service.guardar_objetivos(7, [self.objetivo(code="999")], db)

        self.assertEqual([r.id_agreement for r in creados], [7, 7, 7])
        self.assertEqual([r.id_product for r in creados], [None, 10, 11])
        self.assertEqual(creados[0].code, "10")
        self.assertEqual(creados[2].state_id, 1)
        self.assertEqual(creados[2].quantity, Decimal("2.50"))
        self.assertEqual(creados[2].observations, "Entrega parcial")
        db.commit.assert_not_called()

    def test_preserva_ids_y_estado_de_registros_existentes(self):
        filas = [
            SimpleNamespace(id=1, id_product=None, code="1", product="Objetivo"),
            SimpleNamespace(id=2, id_product=1, code="1.1", product="Actividad"),
            SimpleNamespace(id=3, id_product=2, code="P1", product="Producto", state_id=5),
        ]
        objetivo = self.objetivo(id=1)
        objetivo.actividades[0].id = 2
        objetivo.actividades[0].productos[0].id = 3
        db = Mock()
        with patch.object(service, "listar_registros", return_value=filas):
            service.guardar_objetivos(7, [objetivo], db)
        db.add.assert_not_called()
        self.assertEqual(filas[2].state_id, 5)

    def test_rechaza_ids_ajenos_y_padres_incorrectos(self):
        for filas in [[], [SimpleNamespace(id=99, id_product=22, code="1")]]:
            with self.subTest(filas=filas), \
                    patch.object(service, "listar_registros", return_value=filas), \
                    self.assertRaises(ValueError):
                service.guardar_objetivos(7, [self.objetivo(id=99)], Mock())

    def test_rechaza_producto_con_codigo_duplicado_entre_hermanos(self):
        objetivo = self.objetivo()
        objetivo.actividades[0].productos.append(objetivo.actividades[0].productos[0].model_copy())
        with patch.object(service, "listar_registros", return_value=[]), \
                self.assertRaises(ValueError):
            service.guardar_objetivos(7, [objetivo], Mock())

    def test_carga_jerarquia_y_admite_campos_nulos_heredados(self):
        filas = [
            SimpleNamespace(id=3, id_product=2, code="P1", product="Producto",
                            unit_measure=None, quantity=None, observations=None, state_id=4),
            SimpleNamespace(id=2, id_product=1, code="1.1", product="Actividad"),
            SimpleNamespace(id=1, id_product=None, code="1", product="Objetivo"),
        ]
        with patch.object(service, "listar_registros", return_value=filas):
            objetivos = service.obtener_objetivos(7, Mock())
        self.assertEqual(objetivos[0]["actividades"][0]["productos"][0]["id"], 3)
        self.assertIsNone(objetivos[0]["actividades"][0]["productos"][0]["quantity"])

    def test_creacion_guarda_jerarquia_antes_del_primer_commit(self):
        estudio = SimpleNamespace(
            id=12, capacity_assessment=None, persons=None, implementers=None, programs=None,
        )
        db = Mock()
        eventos = []
        db.commit.side_effect = lambda: eventos.append("commit")
        payload = PreviousStudiesCreate(objetivos=[self.objetivo()])
        with patch.object(studies.UsuariosRepository, "obtener_por_guid_msft",
                          return_value=SimpleNamespace(id=3, email=None)), \
                patch.object(studies.PreviousStudiesRepository, "numero_estudios_previos", return_value=1), \
                patch.object(studies, "PreviousStudiesEntity", return_value=estudio), \
                patch.object(studies.AgreementssService, "crear_agreement",
                             return_value=ResponseRequest(solicitud_exitosa=True, identity=7)) as crear, \
                patch.object(service, "guardar_objetivos", side_effect=lambda *args: eventos.append("productos")), \
                patch.object(studies.SolicitudesAprobacionService, "obtener_categoria_aprobacion", return_value=1), \
                patch.object(studies.SolicitudesAprobacionService, "crear_solicitud_aprobacion", return_value=23):
            respuesta = studies.crearEstudioPrevio(payload, db, "usuario", BackgroundTasks())
        self.assertTrue(respuesta.solicitud_exitosa, respuesta.mensaje)
        self.assertEqual(eventos[0], "productos")
        self.assertEqual(crear.call_args.kwargs, {"confirmar": False})

    def test_error_de_productos_revierte_creacion_sin_confirmar_estudio(self):
        estudio = SimpleNamespace(id=12, capacity_assessment=None)
        db = Mock()
        with patch.object(studies.UsuariosRepository, "obtener_por_guid_msft",
                          return_value=SimpleNamespace(id=3)), \
                patch.object(studies.PreviousStudiesRepository, "numero_estudios_previos", return_value=1), \
                patch.object(studies, "PreviousStudiesEntity", return_value=estudio), \
                patch.object(studies.AgreementssService, "crear_agreement",
                             return_value=ResponseRequest(solicitud_exitosa=True, identity=7)), \
                patch.object(service, "guardar_objetivos", side_effect=ValueError("Error de productos")):
            respuesta = studies.crearEstudioPrevio(
                PreviousStudiesCreate(objetivos=[self.objetivo()]), db, "usuario", BackgroundTasks()
            )
        self.assertFalse(respuesta.solicitud_exitosa)
        self.assertIn("Error de productos", respuesta.mensaje)
        db.rollback.assert_called_once()
        db.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
