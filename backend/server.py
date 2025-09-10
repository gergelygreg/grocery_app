from flask import Flask, request, jsonify
import products_dao, uom_dao, orders_dao
import json
from sql_connection import get_sql_connection
from flask_cors import CORS
import os
from flask import send_from_directory


landing_page_dir = r"C:\Users\Gergely\Desktop\GitRepo\grocery_app\ui"

app = Flask(__name__, static_folder=landing_page_dir, static_url_path="")
CORS(app) # lets all origins hit your API

connection = get_sql_connection()



@app.route("/", methods=["GET"])
def index():
    return send_from_directory(landing_page_dir, "index.html")

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProducts', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    products = uom_dao.get_uoms(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=["POST"])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify ({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    products = orders_dao.get_all_orders(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server for Grocery Store Management System")
    app.run(host="127.0.0.1", port=5000)