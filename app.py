from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages
client = MongoClient('mongodb+srv://jagjegadesh:8667822518Jio@cluster0.rkzhp7w.mongodb.net/')
db = client['store']  # Replace 'store' with your actual database name

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check username and password (you would typically validate against a database here)
        # For demo purposes, let's assume username and password are correct
        return render_template('dashboard.html')

    # Handle GET request to /dashboard
    # You may want to fetch and display some initial data here
    data = list(db.data.find())  # Fetch all data from MongoDB
    return render_template('dashboard.html', data=data)

@app.route('/save_data', methods=['POST','GET'])
def save_data():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        data = {
            'name': name,
            'amount': amount,
            'time': current_time,
            'date': current_date
        }
        db.data.insert_one(data)  # Insert data into MongoDB collection
        # flash("Data saved successfully", "success")  # Flash success message
        return redirect(url_for('dashboard'))  # Redirect back to the dashboard
    return render_template('dashboard.html',data=data)

@app.route('/search_and_filter', methods=['GET'])
def search_and_filter():
    search_name = request.args.get('search_name')
    filter_date = request.args.get('filter_date')
    query = {}
    if search_name:
        query['name'] = search_name
    if filter_date:
        query['date'] = filter_date
    search_results = list(db.data.find(query))
    return render_template('dashboard.html', search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)

