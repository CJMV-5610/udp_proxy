FROM ubuntu

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y dnsutils
RUN apt-get install iputils-ping -y
RUN apt-get install netcat -y

EXPOSE 20000
EXPOSE 30000

COPY ./udp_proxy.py ./udp_proxy.py
COPY ./packet_decoder.py ./packet_decoder.py
COPY ./entrypoint.sh ./entrypoint.sh

CMD ["./entrypoint.sh"]
