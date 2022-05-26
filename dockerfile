FROM python:3.10.4 as builder

USER root

WORKDIR /app/

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip install -Ur requirements.txt

FROM python:3.10.4-slim-buster as deploy

WORKDIR /app/

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/

RUN apt-get update -y

RUN apt-get install gcc -y

ENTRYPOINT [ "python","main.py" ]
