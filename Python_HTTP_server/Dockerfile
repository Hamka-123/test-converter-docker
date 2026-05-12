FROM python:3.14-alpine
WORKDIR /app
EXPOSE 8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app .
#CMD ["python","start_server.py"]