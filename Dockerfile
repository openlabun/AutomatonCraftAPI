# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app/automatonAPI/

# Copia el contenido de tu proyecto al contenedor
COPY . /app/

# Copia el archivo requirements.txt y lo instala
RUN pip install -r requirements.txt



# Exponer el puerto 5020
EXPOSE 5020 8000

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Correr lanzar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
