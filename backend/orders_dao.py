from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")

    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO orders_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
    order_details_data = []
    for order_details_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_details_record['product_id']),
            float(order_details_record['quantity']),
            float(order_details_record['total_price'])
        ])


    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)

    response = []
    for (order_id, customer_name, total, datetime) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': datetime
        })
    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(insert_order(connection, {
        'customer_name': 'Brian Johnson',
        'grand_total': '45',
        #'datetime': datetime.now(),
        'order_details': [
            {
                'product_id': 1,
                'quantity': 2,
                'total_price': 10
            },
            {
                'product_id': 2,
                'quantity': 1,
                'total_price': 5
            },
            {
                'product_id': 6,
                'quantity': 10,
                'total_price': 2
            }   
        ]}
    ))
    