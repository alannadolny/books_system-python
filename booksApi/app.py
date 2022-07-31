from pydoc import cli
from flask import Flask, request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json

client = MongoClient('mongodb://mongo:27017/')
validator = json.load(open('validation.json'))

myDB = client['books']
if 'collection' not in myDB.list_collection_names():
    myDB.create_collection('collection')

client.books.command('collMod', 'collection', validator=validator, validationLevel='moderate')
app = Flask(__name__)


@app.route("/books", methods=['GET'])
def get_books():
    try:
        documents = client.books.collection.find()
        return {"data": list(map(lambda x: json.loads(json_util.dumps(x)), list(documents)))}
    except:
        return abort(500)


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        document = client.books.collection.find_one({'_id': ObjectId(book_id)})
        to_return = {"data": json.loads(json_util.dumps(document))} if document is not None else {"data": "not found"}
        return to_return
    except:
        return abort(500)


@app.route("/books", methods=['POST'])
def post_book():
    try:
        content_type = request.headers.get('Content-Type')
        data = request.json if content_type == 'application/json' else json.loads(json.dumps(request.form))
        inserted_id = client.books.collection.insert_one(data).inserted_id
        data['_id'] = str(inserted_id)
        return data
    except:
        return abort(500)


@app.route("/books/<id_to_delete>", methods=['DELETE'])
def delete_book(id_to_delete):
    try:
        client.books.collection.delete_one({'_id': ObjectId(id_to_delete)})
        return {'deletedId': id_to_delete}
    except:
        return abort(500)


@app.route("/books/<id_to_update>", methods=['PUT'])
def update_book(id_to_update):
    try:
        content_type = request.headers.get('Content-Type')
        data = request.json if content_type == 'application/json' else json.loads(json.dumps(request.form))
        client.books.collection.find_one_and_update({"_id": ObjectId(id_to_update)},
                                                    {'$set': data})
        return str(data)
    except:
        return abort(500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
