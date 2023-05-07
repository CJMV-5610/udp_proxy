FROM alpine

WORKDIR /app

RUN apk update
RUN apk add python3

EXPOSE 20000
EXPOSE 30000

COPY ./udp_proxy.py ./udp_proxy.py

CMD ["python3", "-u", "udp_proxy.py", "30000", "20000"]
