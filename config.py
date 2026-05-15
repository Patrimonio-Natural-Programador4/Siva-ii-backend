import os

# Base storage path for files.
# Evaluates to "" (empty string) in local dev, acting as relative to root.
# Evaluates to the Docker volume mount path, e.g., "/app/data/", in Production.
STORAGE_PATH = os.getenv("ruta_disco", "")
