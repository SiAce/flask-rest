import sqlite3

from flask_jwt import jwt_required
from flask_restful import reqparse, Resource


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True)

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'An item with name: <{}> already exists.'.format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        self.insert_by_item(item)

        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item {} deleted'.format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        update_item = {'name': name, 'price': data['price']}

        if item is None:
            self.insert_by_item(update_item)
        else:
            self.update(update_item)

        return update_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def insert_by_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        item_list = [{'name': row[0], 'price': row[1]} for row in result]

        connection.close()

        return {'items': item_list}
