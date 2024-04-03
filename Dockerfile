FROM python:3.6
WORKDIR /opentalents
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /opentalents
RUN apt-get update && apt-get install -y xvfb wkhtmltopdf graphviz
RUN pip install -r requirements.txt
