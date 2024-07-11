# from flask import Flask, render_template, request, redirect, url_for,flash
# from pymongo import MongoClient
# from datetime import datetime

# app = Flask(__name__)
# # app.secret_key='e5f6a8c2f7d4a1b8c3d2e1f4a7c6b2d8'
# client = MongoClient('mongodb://localhost:27017/')
# db = client['store']  # Replace 'your_database_name' with your actual database name

# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/dashboard', methods=['POST','GET'])
# def dashboard():
#   if request.method == 'POST':
#     username = request.form['username']
#     password = request.form['password']
#     # Check username and password (you would typically validate against a database here)
#     # For demo purposes, let's assume username and password are correct
#     return render_template('dashboard.html')
# #   return render_template('login.html')
   
# @app.route('/save_data', methods=['POST','GET'])
# def save_data():
#     if request.method == 'POST':
#         name = request.form['name']
#         amount = request.form['amount']
#         now = datetime.now()
#         current_time = now.strftime("%H:%M:%S")
#         current_date = now.strftime("%Y-%m-%d")
#         data = {
#             'name': name,
#             'amount': amount,
#             'time': current_time,
#             'date': current_date
#         }
#         db.data.insert_one(data)  # Insert data into MongoDB collection
#         # flash("Data saved  sucessfully")
#         # return redirect(url_for('dashboard'))
#     return render_template('dashboard.html')
# @app.route('/search_data', methods=['GET'])
# def search_data():
#     search_name = request.args.get('search_name')
#     search_results = list(db.data.find({'name': search_name}))
#     return render_template('dashboard.html', search_results=search_results)
# @app.route('/filter_by_date', methods=['GET'])
# def filter_by_date():
#     filter_date = request.args.get('filter_date')
#     filtered_results = list(db.data.find({'date': filter_date}))
#     return render_template('filtered_results.html', filtered_results=filtered_results)


# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
# from pymongo import MongoClient
# from datetime import datetime

# app = Flask(__name__)
# # app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages
# client = MongoClient('mongodb://localhost:27017/')
# db = client['store']  # Replace 'store' with your actual database name

# @app.route('/')
# def login():
#     return render_template('login.html')

# @app.route('/dashboard', methods=['POST', 'GET'])
# def dashboard():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # Check username and password (you would typically validate against a database here)
#         # For demo purposes, let's assume username and password are correct
#         return render_template('dashboard.html')

#     # Handle GET request to /dashboard
#     # You may want to fetch and display some initial data here
#     # For example:
#     data = list(db.data.find())  # Fetch all data from MongoDB
#     return render_template('dashboard.html', data=data)

# @app.route('/save_data', methods=['POST'])
# def save_data():
#     if request.method == 'POST':
#         name = request.form['name']
#         amount = request.form['amount']
#         now = datetime.now()
#         current_time = now.strftime("%H:%M:%S")
#         current_date = now.strftime("%Y-%m-%d")
#         data = {
#             'name': name,
#             'amount': amount,
#             'time': current_time,
#             'date': current_date
#         }
#         db.data.insert_one(data)  # Insert data into MongoDB collection
#         # flash("Data saved successfully", "success")  # Flash success message
#         return redirect(url_for('dashboard'))  # Redirect back to the dashboard

# @app.route('/search_data', methods=['GET'])
# def search_data():
#     search_name = request.args.get('search_name')
#     search_results = list(db.data.find({'name': search_name}))
#     return render_template('dashboard.html', search_results=search_results)

# @app.route('/filter_by_date', methods=['GET'])
# def filter_by_date():
#     filter_date = request.args.get('filter_date')
#     filtered_results = list(db.data.find({'date': filter_date}))
#     return render_template('filtered_results.html', filtered_results=filtered_results)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages
client = MongoClient('mongodb://localhost:27017/')
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
        return redirect(url_for('dashboard.html'))  # Redirect back to the dashboard
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

