FROM ubuntu:latest

RUN apt update; apt install software-properties-common -y; add-apt-repository ppa:deadsnakes/ppa -y; apt install python3.9 -y; apt install python3-pip -y; apt install git -y;
RUN pip install biopython pika==1.1.0 rabbitmq-tool amqp_client_cli pandas pymongo sqlAlchemy pymysql joblib
RUN pip install mysql-connector-python

COPY . /tmp/

#ENTRYPOINT ["python3", "/tmp/GenomInfo.py"]