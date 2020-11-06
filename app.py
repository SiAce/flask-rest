from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [{'name': 'trash', 'price': 15.99},
                  {'name': 'water', 'price': 1.99},
                  {'name': 'chips', 'price': 3.99}]
    },
    {
        'name': 'Amazon',
        'items': [{'name': 'computer', 'price': 1199.99},
                  {'name': 'computer', 'price': 1199.99}]
    },
    {
        'name': 'Google',
        'items': [{'name': 'pixel5', 'price': 499.99}]
    }
]


@app.route('/')
def home():
    return 'Hello World!'


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'item': []
    }

    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': "store not found"})


@app.route('/store')
def get_stores():
    return jsonify({"stores": stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})

    return jsonify({'message': "store not found"})


@app.route('/store/<string:name>/item', methods=['GET'])
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()
            new_item = request_data['item']
            stores['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': "store not found"})


if __name__ == '__main__':
    app.run()
