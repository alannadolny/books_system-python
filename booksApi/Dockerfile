FROM python

WORKDIR /opt/booksApi

COPY . .

RUN pip3 install flask

RUN pip3 install pymongo

CMD [ "python", "app.py" ]