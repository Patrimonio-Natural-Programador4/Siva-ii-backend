# Estructura de parámetros Word

Para que el servicio extraiga información de un documento, cree una tabla de dos columnas en Word.
La primera fila debe ser exactamente el encabezado `NOMBRE` y `VALOR`.
Cada fila siguiente representa un parámetro.

| NOMBRE | VALOR |
| --- | --- |
| rubro | 765 |
| No. PROCESO | AB23C123 |
| Lugar De Ejecución | Las labores serán realizadas en Bogotá. |

Se puede usar más de una tabla de parámetros en el mismo documento. Solo se procesan las tablas con encabezado `NOMBRE | VALOR`; por compatibilidad, también se interpreta una tabla sin encabezado de exactamente dos columnas como pares de parámetros.
Las celdas pueden contener párrafos y saltos de línea; el servicio los devuelve como un solo espacio.

El documento de ejemplo también se procesa porque usa una tabla de dos columnas sin encabezado, donde cada fila es un par `nombre | valor`. Para plantillas nuevas se recomienda la tabla con encabezado, ya que evita procesar por error tablas de dos columnas que no sean parámetros.

Los parámetros que el servicio debe devolver se configuran en el array `_PARAMETROS_DESEADOS` de `services/WordParametersService.py`. La misma lista se aplica tanto a tablas como a párrafos. Por compatibilidad con el documento de ejemplo, un parámetro de esa lista también se extrae cuando aparece como un párrafo independiente, terminado en `.` o `:`, y el valor está en el párrafo siguiente.

El formato recomendado es `.docx`. También se aceptan `.doc`: el servicio los convierte temporalmente a `.docx` mediante LibreOffice en modo sin interfaz. Para instalaciones Linux fuera de Docker, instale `libreoffice-writer`.

## Endpoint

Envíe el archivo como `multipart/form-data` usando el campo `archivo`:

```http
POST /documentos/extraer-parametros
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

La respuesta tiene esta forma:

```json
{
  "parametros": [
    {"nombre": "rubro", "valor": "765"},
    {"nombre": "No. PROCESO", "valor": "AB23C123"}
  ]
}
```