FROM postgres:alpine

# RUN apk update && apk add postgresql-client

# install python for execute python scripts

ADD ./crontab.txt /crontab.txt
COPY ./entrypoint.sh /entrypoint.sh
COPY ./cron.py /cron.py

RUN chmod 755  /entrypoint.sh
RUN /usr/bin/crontab /crontab.txt
RUN madir -p /data/backups

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" >  /etc/timezone

RUN apk update && \
    apk add python && \
    apk add py-pip && \
    pip install qiniu

ENTRYPOINT "/entrypoint.sh"