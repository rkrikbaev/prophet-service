FROM fpcloud/prophet-env-amd64:v1.0

LABEL Auth: Krikbayev Rustam 
LABEL Email: "rkrikbaev@gmail.com"
ARG SERVICE_VERSION=v1.1.4

ENV REFRESHED_AT 2020-11-20

RUN pip install --upgrade pip

RUN pip install falcon==3.0.1 && \
    pip install jsonschema

RUN pip install pyinstaller

EXPOSE 8005

RUN mkdir application
WORKDIR /application
COPY ./service /application

RUN mkdir logs

CMD ["python", "app.py"]