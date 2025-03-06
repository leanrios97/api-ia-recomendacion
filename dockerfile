# Establece la imagen base para Python
FROM python:3.11.5

# Configura el entorno de trabajo
WORKDIR /gemini_api

# Instala curl y Rust
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y nano


# Copia los archivos de tu aplicación Python al contenedor
COPY . /gemini_api
COPY resolv.conf /etc/

# Instala las dependencias de Python
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install python-dotenv
RUN pip install pymongo


# Exponemos el puerto en el que la aplicación FastAPI escuchará
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8080"] 