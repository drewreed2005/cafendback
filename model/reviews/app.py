from flask import Flask, request, jsonify
import json
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/average/*": {"origins": "*"}})
cors = CORS(app, resources={r"/getrev/*": {"origins": "*"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('reviews.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/reviews', methods=['GET', 'POST'])
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
        print("POst method works")
        new_name = request.json['name']
        new_review = request.json['review']
        new_rate = request.json['rate']
        sql = """INSERT INTO reviews (name, review, rate)
                 VALUES (?, ?, ?)"""
        cursor = conn.execute(sql, (new_name, new_review, new_rate))
        conn.commit()
        return f"Review created successfully", 201

@app.route('/delete/<id>', methods = ["GET"])
def delete_review(id):
    message = {}
    if request.method == 'GET':
        try:
            conn = db_connection()
            conn.execute("DELETE from reviews WHERE id = ?",
                     (id,))
            conn.commit()
            message["status"] = "User deleted successfuly"
        except:
            message["status"] = "error cant delete user"
        return message

@app.route('/getrev', methods=['GET'])
def getreviews():
   if request.method == "GET": 
        conn = db_connection()
        cursor = conn.cursor
        rate = None
        cursor = conn.execute("SELECT * FROM reviews")
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews is not None:
            return jsonify(reviews)
    

    


@app.route('/average', methods=['GET'])
def average_rate():
   if request.method == "GET": 
        conn = db_connection()
        cursor = conn.cursor
        rate = None
        cursor = conn.execute("SELECT round(avg(rate),2) FROM reviews")
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                rate = row[0]
           # response = 
           # response.headers.add('Access-Control-Allow-Origin', '*')
            return str(rate)
        else:
            return "Something wrong", 404


    

# if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=8239)