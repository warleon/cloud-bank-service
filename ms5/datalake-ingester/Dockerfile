# Dockerfile para el contenedor de ingesta
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts de ingesta
COPY ingester.py .
COPY run_ingestion.py .

# Comando por defecto (será sobrescrito por docker-compose)
CMD ["python", "run_ingestion.py"]