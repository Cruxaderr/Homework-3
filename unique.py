from flask import Flask, render_template_string 
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

db_config = {
        'host': 'localhost',
        'database': 'dvdrental',
        'user': 'raywu1990',
        'password': 'test'
}

@app.route('/api/unique', methods=['GET'])
def unique_fruits():
	try:
		connection = psycopg2.connect(**db_config)
		cursor = connection.cursor()


		query_a = """
		SELECT fruit_a FROM basket_a
		WHERE NOT EXISTS (SELECT fruit_b FROM basket_b WHERE
		basket_b.fruit_b = basket_a.fruit_a);
		"""
		query_b = """
		SELECT fruit_b FROM basket_b
		WHERE NOT EXISTS (SELECT fruit_a FROM basket_a WHERE
		basket_a.fruit_a = basket_b.fruit_b);
		"""

		cursor.execute(query_a)
		unique_a = cursor.fetchall()
		
		cursor.execute(query_b)
		unique_b = cursor.fetchall()

		

		html = """
		<html>
			<head>
				<title>Unique Fruits</title>
				<style>
					table { width: 50%; margin: 20px auto; border-collapse: collapse; }
					th, td { border: 1px solid black; padding: 8px; text-align: center; }
					th { background-color: #f2f2f2; }
				</style>
			</head>
			<body>
				<h2 style="text-align: center;">Unique Fruits</h2>
				<table>
					<tr>
						<th>Basket A</th>
						<th>Basket B</th>
					</tr>
		"""


		max_len = max(len(unique_a), len(unique_b))
		for i in range(max_len):
			fruit_a = unique_a[i][0] if i < len(unique_a) else ''
			fruit_b = unique_b[i][0] if i < len(unique_b) else ''
			html += f"<tr><td>{fruit_a}</td><td>{fruit_b}</td></tr>"
		html += """
				</table>
			</body>
		</html>
		"""

		cursor.close()
		connection.close()

		return render_template_string(html), 200
	except Exception as e:
		return str(e), 500

if __name__ == '__main__':
	app.run(debug=True)
