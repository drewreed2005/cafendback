from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('reviews.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/', methods=['GET', 'POST'])
def reviews():
    conn = db_connection()
    cursor = conn.cursor
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM reviews")
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews is not None: 
            return jsonify(reviews)


    if request.method == 'POST':
        new_name = request.form['name']
        new_review = request.form['review']
        new_rate = request.form['rate']
        sql = """INSERT INTO reviews (name, review, rate)
                 VALUES (?, ?, ?)"""
        cursor = conn.execute(sql, (new_name, new_review, new_rate))
        conn.commit()
        return f"Review created successfully", 201

@app.route('/average')
def average_rate():
    conn = db_connection()
    cursor = conn.cursor
    rate = None
    cursor = conn.execute("SELECT avg(rate) FROM reviews")
    rate = cursor.fetchall()
    if rate is not None:
        return rate
    else:
        return "Something wrong", 404

if __name__ == "__main__":
    app.run(debug=True)