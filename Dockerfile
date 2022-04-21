FROM fpcloud/prophet-env-amd64:v1.0

LABEL Auth: Krikbayev Rustam
LABEL Email: "rkrikbaev@gmail.com"

ENV REFRESHED_AT 2020-11-20

RUN pip install --upgrade pip

COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt 
# RUN pip install falcon==3.0.1 && \
#     pip install jsonschema \
#     pip install gunicorn

VOLUME [ "/mlruns" ]

EXPOSE 8005

RUN mkdir application
WORKDIR /application

COPY ./web_app .

CMD ["sh", "entry_point.sh"]