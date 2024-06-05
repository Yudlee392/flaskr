import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)


DATABASE_CONFIG = {
    'database': 'db',
    'user': 'thiendeptrai',
    'password': '123456',
    'host': '10.10.31.153', 
    'port': 5432
}

def get_db_connection():
    """Connect to PostgreSQL"""
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_data():
    if request.method == 'GET':
        # Read data
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM student")
                data = cur.fetchall()
        return jsonify(data)

    elif request.method == 'POST':
        # Create data
        new_data = request.get_json()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO student (name, age) VALUES (%s, %s)", 
                            (new_data['name'], new_data['age']))
            conn.commit()
        return jsonify({'message': 'Data created successfully'})

    elif request.method == 'PUT':
        # Update data
        update_data = request.get_json()
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE student SET name = %s, age = %s WHERE id = %s", 
                            (update_data['name'], update_data['age'], update_data['id']))
            conn.commit()
        return jsonify({'message': 'Data updated successfully'})

    elif request.method == 'DELETE':
        # Delete data
        data_id = request.args.get('id')
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM student WHERE id = %s", (data_id,))
            conn.commit()
        return jsonify({'message': 'Data deleted successfully'})
    return app
if __name__ == 'main':
    app.run(port=5000, debug=True)
