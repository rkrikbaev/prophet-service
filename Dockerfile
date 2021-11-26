FROM fpcloud/prophet-env-amd64:latest

LABEL Auth: Krikbayev Rustam 
LABEL Email: "rkrikbaev@gmail.com"

ENV REFRESHED_AT 2020-11-20

RUN pip install --upgrade pip

RUN pip install falcon==3.0.1 && \
    pip install jsonschema

EXPOSE 8005

RUN mkdir application
WORKDIR /application
COPY ./service /application

RUN mkdir logs

CMD ["/bin/bash", "start.sh"]