FROM rkrikbaev/pyinstaller_prophet:v1.0.1

ARG SERVICE_VERSION=v1.0.0

RUN pip install falcon==3.0.1

EXPOSE 8005

RUN mkdir application
WORKDIR /application
COPY . /application

RUN mkdir logs

CMD ["python", "app.py"]