#Aspectos a tener en cuenta para trabajar con este repositorio

1. Tener instalado python se recomienda version ( 11 o 12)
2. Ejecutar los siguientes comandos:

   ```
   a. Crear entorno virtual ->  python -m venv venv
   b. Inicializar entorno virtual -> venv\Scripts\activate
   c. Instalación de dependencias:
        - pip install fastapi uvicorn
        - pip install sqlalchemy psycopg2-binary python-dotenv
        - pip install fastapi-microsoft-identity
        - pip install pyjwt
        - pip install msal

   ```

3. Comando para subir API:

   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8111

   ```

4. Para que la visualización pdf funione se deben seguir los siguientes pasos

   ```
      1. Instalar Gtk3-runtime.  https://github.com/tschoonj/  GTK-for-Windows-Runtime-Environment-Installer/releases
      2.Configurar variable de entorno:
             - nombre variable : WEASYPRINT_DLL_DIRECTORIES
             - Ubicacion ejemplo: C:\Program Files\GTK3-Runtime Win64\bin
      3. Reiniciar la consola y probar con lo siguiente :
          - echo %WEASYPRINT_DLL_DIRECTORIES%

      4. Subir back y probar en el sistema

   ```

## Objetivos, actividades y productos de estudios previos

Los endpoints `POST /estudios-previos` y `PUT /estudios-previos/{guid}` aceptan
`objetivos`, una lista de objetos con `product` y `actividades`. Cada actividad
incluye `code`, `product` y `productos`. Cada producto incluye `code`, `product`,
`unit_measure`, `quantity` (no negativa, hasta dos decimales) y `observations`
(opcional).

La jerarquia se guarda en `agreements_products`: `id_agreement` identifica el
acuerdo del estudio y `id_product` identifica al padre (nulo para objetivos).
Los objetivos nuevos reciben un codigo consecutivo; los productos nuevos tienen
`state_id = 1`. El detalle `GET /estudios-previos/{guid}/detalle` devuelve
`objetivos` con los mismos niveles y los IDs persistidos.

El paso 4 permite agregar registros y editar nombres de objetivos y codigo/nombre
de actividades, y codigo, nombre, unidad, cantidad y observaciones de productos
mediante el drawer. Los cambios se guardan junto con el estudio;
los nodos editados envian `modificar: true`. Se conservan IDs, padres, hijos,
estados y campos heredados. No se eliminan registros. Al reenviar
IDs existentes se validan el acuerdo y el padre, sin sobrescribir estados ni
otros datos heredados. Omitir `objetivos` o enviar una lista vacia no borra
registros. Los cambios se guardan junto con el formulario, no al cerrar el drawer.
No se requiere la columna temporal `session` para este flujo.

## Desembolsos de estudios previos

El quinto paso permite agregar desembolsos con numero (entero positivo), fecha
programada, valor no negativo (hasta dos decimales), estado, fechas de
solicitud/validacion/aprobacion/desembolso, documento soporte, observaciones y
al menos un producto de nivel 3. Los estados se consultan mediante
`GET /estudios-previos/catalogos/estados-desembolso`.

El mismo POST/PUT del estudio acepta `desembolsos`. Cada entrada utiliza
`product_keys`: `id:123` para un producto existente o `new:referencia` para un
producto creado en el mismo formulario. En este ultimo caso, el producto del
arbol lleva `client_id: "referencia"`; es una referencia temporal de la solicitud,
no una nueva columna. El backend resuelve los IDs antes de guardar en
`disbursement` y `disbursement_products` dentro de la misma transaccion.

No se permite asociar un producto a mas de un desembolso, ni usar objetivos,
actividades o productos ajenos al acuerdo. El drawer permite editar desembolsos
nuevos y existentes; los cambios se aplican al guardar el estudio. Las entradas
con `id` y datos completos actualizan el desembolso y sus asociaciones, conservando
su identidad y fecha de creacion. Enviar solo `id` conserva el registro sin cambios.
El pie de la tabla muestra la suma de los valores y el arbol del paso 4 inicia
contraido. El detalle del estudio devuelve
`desembolsos` con las referencias persistidas. Omitir la lista no elimina datos.
