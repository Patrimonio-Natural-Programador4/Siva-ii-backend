from pathlib import Path

from docx import Document
from docx.text.paragraph import Paragraph

from config import STORAGE_PATH
from services.TdrDocumentService import _PATRON_HTML, _html_a_texto, _reemplazar_en_parrafo


def generar_formato_ep(diccionario: dict[str, object], code: str) -> Path:
    base = Path(STORAGE_PATH or Path(__file__).resolve().parents[1])
    directorio = base / "soportes" / "acuerdos" / "estudios_previos"
    plantilla = directorio / "template" / "plantilla_estudios_previos.docx"
    documento = Document(str(plantilla))
    valores = {
        marcador.removeprefix("<<").removesuffix(">>"): _html_a_texto(
            str(valor) if valor is not None else ""
        )
        for marcador, valor in diccionario.items()
    }
    valores_html = {
        marcador.removeprefix("<<").removesuffix(">>"): valor
        for marcador, valor in diccionario.items()
        if isinstance(valor, str) and _PATRON_HTML.search(valor)
    }
    partes = [documento.part]
    for seccion in documento.sections:
        for contenedor in (
            seccion.header, seccion.first_page_header, seccion.even_page_header,
            seccion.footer, seccion.first_page_footer, seccion.even_page_footer,
        ):
            if not contenedor.is_linked_to_previous and contenedor.part not in partes:
                partes.append(contenedor.part)
    for parte in partes:
        for elemento in list(parte.element.xpath(".//w:p")):
            parrafo = Paragraph(elemento, parte)
            for fragmento in parrafo.runs:
                if "<<ALCANCE>" in fragmento.text and "<<ALCANCE>>" not in fragmento.text:
                    fragmento.text = fragmento.text.replace("<<ALCANCE>", "<<ALCANCE>>")
            _reemplazar_en_parrafo(parrafo, valores, valores_html)

    codigo_archivo = "".join(
        caracter if caracter.isalnum() or caracter in "-_" else "_"
        for caracter in str(code)
    )
    salida = directorio / "formato" / f"ep_{codigo_archivo}.docx"
    salida.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(salida))
    return salida