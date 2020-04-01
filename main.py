from flask import Flask, request, jsonify
from datetime import datetime
from google.cloud import datastore
import os

# init app
app = Flask(__name__)

# init DataStore

datastore_client = datastore.Client()

@app.route('/')
def root():
    return "Rest Api with google app engine, google datastore and Flask"

# Create a BDay
@app.route('/bday', methods=['POST'])
def addBDay():
    bday = datastore.Entity(key=datastore_client.key('BDay'))
    bday.update({
        'name': request.json['name'],
        'fname': request.json['fname'],
        'date': request.json['date']
    })
    datastore_client.put(bday)
    return jsonify(success={'id': bday.key.id, 'kind':bday.key.kind})

# Get All BDay
@app.route('/bday', methods=['GET'])
def get_bdays():
    query = datastore_client.query(kind='BDay')
    bdays = query.fetch()
    list = []
    for i in bdays:
        list.append({'id': i.key.id, 'kind': i.key.kind, 'fields': {a: b for a, b in i.items()}})
    return jsonify(list)

# Get One BDay
@app.route('/bday/<id>', methods=['GET'])
def get_bday(id):
    key = datastore_client.key('BDay', int(id))
    bday = datastore_client.get(key)
    if bday:
        return jsonify({a: b for a, b in bday.items()})
    return jsonify(error="Bday not found")


# Delete Bday
@app.route('/bday/<id>', methods=['DELETE'])
def delete_bday(id):
    key = datastore_client.key('BDay', int(id))
    datastore_client.delete(key)
    return jsonify(success='Bday Deleted')

# Update a BDay
@app.route('/bday/<id>', methods=['PUT'])
def update_product(id):
    key = datastore_client.key('BDay', int(id))
    bday = datastore_client.get(key)
    if bday:
        bday['name'] = request.json['name']
        bday['fname'] = request.json['fname']
        bday['date'] = request.json['date']

        datastore_client.put(bday)
        return jsonify(success="Bday Updated")
    return jsonify(error="BDay not found")

# Run server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,debug=True)
