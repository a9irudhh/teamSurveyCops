from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = '&%#$@56'  # Replace with a strong secret key

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Adjust if needed
db = client['student_management']  # Replace with your database name
users = db['users']  # Collection for user credentials

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if users.find_one({'username': username}):
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_password})
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        
        user = users.find_one({'username': username})
        if not user:
            flash('Username not found. Please try again.', 'error')
            return redirect(url_for('forgot_password'))
        
        hashed_password = generate_password_hash(new_password)
        users.update_one({'username': username}, {'$set': {'password': hashed_password}})
        flash('Password reset successful! You can now log in with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

if __name__ == '__main__':
    app.run(debug=True)
