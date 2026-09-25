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
