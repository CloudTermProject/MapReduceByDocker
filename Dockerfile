FROM python:3.10

RUN mkdir -p /opt/myservice
WORKDIR /opt/myservice
COPY . .

EXPOSE 80
CMD python mapper.py