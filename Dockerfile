FROM registry.cn-hongkong.aliyuncs.com/regend/python:flask

MAINTAINER Regend

COPY ./Pjmsg/ /home/Pjmsg/

WORKDIR /home/Pjmsg/

ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT uwsgi uwsgi.ini
