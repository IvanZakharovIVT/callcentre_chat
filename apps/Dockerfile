FROM python:3.14-alpine

# USR_LOCAL_BIN - путь до пользовательских скриптов
# PROJECT_ROOT - путь до каталога внутри контейнера, в который будет
# копироваться приложение
ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/application

# путь до исходников
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

COPY ./requirements.txt $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT