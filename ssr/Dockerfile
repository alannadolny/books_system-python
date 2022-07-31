FROM python:3.10

WORKDIR /opt/ssr

COPY . .

RUN pip3 install flask

RUN pip3 install flask_wtf

RUN pip3 install requests

CMD [ "python", "app.py" ]