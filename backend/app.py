from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)

# Routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "description": p.description} for p in products])

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(product_id=data['product_id'], customer_name=data['customer_name'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order placed successfully!"})

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "product_id": o.product_id, "customer_name": o.customer_name, "quantity": o.quantity} for o in orders])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
