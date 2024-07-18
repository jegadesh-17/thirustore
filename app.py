from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
# app = Flask(__name__, template_folder='static')

app.secret_key = os.urandom(24)  # Set a secret key for flashing messages
client = MongoClient('mongodb+srv://jagjegadesh:8667822518Jio@ac-wvrx6cn-shard-00-01.rkzhp7w.mongodb.net/')
db = client['store']  # Replace 'store' with your actual database name

@app.route('/')
@app.route('/store/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/store/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            data = list(db.data.find())  # Fetch all data from MongoDB
            return render_template('dashboard.html', data=data)
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    else:
        # Handle GET request to /dashboard
        if 'username' in session:
            data = list(db.data.find())  # Fetch all data from MongoDB
            return render_template('dashboard.html', data=data)
        else:
            return redirect(url_for('login'))

@app.route('/store/save_data', methods=['POST'])
def save_data():
    if 'username' in session:
        name = request.form['name']
        amount = request.form['amount']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        data = {
            'name': name,
            'amount': amount,
            'time': current_time,
            'date': current_date,
            'status': 'Unpaid'
        }
        db.data.insert_one(data)  # Insert data into MongoDB collection
        flash("Data saved successfully", "success")
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/store/search_and_filter', methods=['GET'])
def search_and_filter():
    try:
        search_name = request.args.get('search_name')
        filter_date = request.args.get('filter_date')
        query = {}
        if search_name:
            query['name'] = search_name
        if filter_date:
            query['date'] = filter_date
        search_results = list(db.data.find(query))
        return render_template('search_results.html', filtered_results=search_results)
    except Exception as e:
        print("Error fetching data:", str(e))
        return render_template('search_results.html', filtered_results=[], error_message="Error fetching data. Please try again.")

@app.route('/store/update_status', methods=['POST'])
def update_status():
    try:
        data = request.get_json()
        object_id = data.get('id')
        status = data.get('status')
        db.data.update_one({'_id': ObjectId(object_id)}, {'$set': {'status': status}})
        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as e:
        print("Error updating status:", str(e))
        return jsonify({'error': 'Failed to update status'}), 500

@app.route('/store/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = db.users.find_one({'username': username})
        
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('create_user'))
        
        hashed_password = generate_password_hash(password)
        db.users.insert_one({'username': username, 'password': hashed_password})
        flash('User created successfully', 'success')
        return redirect(url_for('login'))
    
    return render_template('create_user.html')

@app.route('/store/all_data', methods=['GET'])
def all_data():
    try:
        all_data = list(db.data.find().sort('date', -1))  # Fetch all data from MongoDB in descending order
        return render_template('search_results.html', filtered_results=all_data)
    except Exception as e:
        print("Error fetching all data:", str(e))
        return render_template('search_results.html', filtered_results=[], error_message="Error fetching all data. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
