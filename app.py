from flask import Flask, render_template, request, url_for, redirect, session
import database_utils
import pymongo
import bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = '64a0f61a16b51b71f9cf959bc11cdf11cb646b40'
db = database_utils.get_database()



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    message = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = db.users.find_one({'username': username})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            message = 'Invalid username or password'
            return render_template('login.html', message=message)
    
    return render_template('login.html')

@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        password2 = request.form['password2']
        
        if db.users.find_one({'username': username}):
            message = 'Username already exists.'
            return render_template('register.html', message=message)
        
        if password1 != password2:
            message =  'Passwords do not match'
            return render_template('register.html', message=message)
        
        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'password': hashed_password,
            'reviews': [],
            'avg_rating': 0.0,
            'is_admin': False    
        }
        
        db.users.insert_one(user_data)
        return 'User registered successfully!'
    
    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True)