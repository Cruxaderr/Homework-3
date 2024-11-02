from flask import Flask 
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

db_config = {
	'host': 'localhost',
	'database': 'dvdrental',
	'user': 'raywu1990',
	'password': 'test'
}

@app.route('/api/update_basket_a', methods=['GET'])
def update_basket_a():
	try:

		connection = psycopg2.connect(**db_config)
		cursor = connection.cursor()

		insert_query = sql.SQL("INSERT INTO basket_a (a, fruit_a) VALUES (%s, %s)")
		cursor.execute(insert_query, (5, 'Cherry'))

		connection.commit()

		cursor.close()
		connection.close()

		return "Success!", 200
	except Exception as e:
		return str(e), 500
if __name__ == '__main__':
	app.run(debug=True)
