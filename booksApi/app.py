from flask import Flask, request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
app = Flask(__name__)


@app.route("/books", methods=['GET'])
def get_books():
    try:
        documents = client.books.collection.find({})
        return str(list(documents))
    except ():
        return abort(500)


@app.route("/books", methods=['POST'])
def post_book():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            inserted_id = client.books.collection.insert_one(data).inserted_id
            data['_id'] = str(inserted_id)
            return data
        else:
            return 'Content-Type not supported!'
    except ():
        return abort(500)


@app.route("/books/<idToDelete>", methods=['DELETE'])
def delete_book(id_to_delete):
    try:
        client.books.collection.delete_one({'_id': ObjectId(id_to_delete)})
        return {'deletedId': id_to_delete}
    except ():
        return abort(500)


if __name__ == '__main__':
    app.run(debug=True)
