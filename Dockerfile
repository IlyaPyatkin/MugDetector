FROM python:3.6.1

# runtime environment

ENV WEB_HOST='localhost'
ENV WEB_PORT='80'

# mount host volumes

COPY ./src /srv

# install application dependencies

RUN cd /srv && pip install -r requirements.txt

WORKDIR /srv/

CMD python server.py
