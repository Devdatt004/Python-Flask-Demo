from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database
items = [
    {'id': 1, "name": "Laptop", "price": 52000},
    {'id': 2, "name": "iPhone", "price": 63000}
]

@app.route("/")
def home():
    return {"message": "Welcome to Flask REST API"}

# GET all items
@app.route("/items", methods=["GET"])
def getitems():
    return jsonify(items)

# GET item by ID
@app.route("/items/<int:itemid>", methods=["GET"])
def getitem(itemid):
    item = next((i for i in items if i['id'] == itemid), None)
    if item:
        return jsonify(item)
    abort(404, description="Item Not Found!")

# POST (Create item)
@app.route("/items", methods=["POST"])
def createitems():
    data = request.json
    if not data or "name" not in data or "price" not in data:
        abort(400, description="Invalid Input!")

    newid = items[-1]['id'] + 1 if items else 1
    item = {
        'id': newid,
        'name': data['name'],
        'price': float(request.json['price'])
    }
    items.append(item)
    return jsonify(item), 201

# PUT (Update item)
@app.route('/items/<int:itemid>', methods=['PUT'])
def update_item(itemid):
    item = next((i for i in items if i['id'] == itemid), None)
    if item is None:
        abort(404, description="Item Not Found!")

    data = request.get_json()
    if not data:
        abort(400, description="Invalid Input!")

    item['name'] = data.get('name', item['name'])
    item['price'] = float(data.get('price', item['price']))
    return jsonify(item)

# DELETE item
@app.route('/items/<int:itemid>', methods=['DELETE'])
def deleteitems(itemid):
    global items
    items = [i for i in items if i['id'] != itemid]
    return jsonify({'message': 'Item Deleted'})


if __name__ == "__main__":
    app.run(debug=True)