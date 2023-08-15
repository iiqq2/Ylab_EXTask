FROM python:3.10-slim

RUN mkdir /ylab_app

RUN pip install --upgrade pip

WORKDIR /ylab_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


CMD ls && gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
EXPOSE 8000
