FROM debian:trixie-20260202-slim

WORKDIR /app
# Update system and install base packages
RUN apt update && apt upgrade -y
RUN apt install bash python3 python3-pip python3-venv -y 

COPY . .

RUN python3 -m venv venv
#RUN /venv/bin/activate
RUN ./venv/bin/pip install -r requirements.txt
RUN pwd

EXPOSE 6969
CMD [ "sh", "-c", "./venv/bin/python -m flask --app hello run --host=0.0.0.0 --port=6969" ]
