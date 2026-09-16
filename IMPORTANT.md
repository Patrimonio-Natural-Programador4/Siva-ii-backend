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
