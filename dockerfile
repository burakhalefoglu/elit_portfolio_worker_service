FROM python:3.10.4-slim-buster

USER root

WORKDIR /elite-portfolio

COPY . /elite-portfolio

RUN python3 -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt

CMD [ "python3 main.py" ]
