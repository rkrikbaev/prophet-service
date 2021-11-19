FROM rkrikbaev/pyinstaller_prophet:v1.0.1

LABEL Auth: Krikbayev Rustam 
LABEL Email: "rkrikbaev@gmail.com"
ARG SERVICE_VERSION=v1.1.4

ENV REFRESHED_AT 2020-10-20

RUN pip install --upgrade pip

RUN pip install falcon==3.0.1 && \
    pip install jsonschema

EXPOSE 8005

RUN mkdir application
WORKDIR /application
COPY ./service /application

RUN mkdir logs

CMD ["python", "app.py"]