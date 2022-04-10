FROM fpcloud/prophet-env-amd64:latest

LABEL Auth: Krikbayev Rustam
LABEL Email: "rkrikbaev@gmail.com"

ENV REFRESHED_AT 2020-11-20

RUN pip install --upgrade pip

RUN pip install falcon==3.0.1 && \
    pip install jsonschema \
    pip install gunicorn

EXPOSE 8005

RUN mkdir application
WORKDIR /application
RUN mkdir model

COPY ./web_app /app

RUN mkdir logs
CMD ["gunicorn"  , "-b", "0.0.0.0:8005", "app:api"]
# CMD ["/bin/bash", "start.sh"]