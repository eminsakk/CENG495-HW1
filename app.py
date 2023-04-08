from flask import Flask, render_template, request, url_for, redirect, session,jsonify
import database_utils
import pymongo
import bcrypt
import time
import json
import os
from bson import ObjectId



app = Flask(__name__)
app.config["SECRET_KEY"] = '64a0f61a16b51b71f9cf959bc11cdf11cb646b40'
db = database_utils.get_database()



###
###   Kalan fonksiyonaliteler:
###   - Userların review yapması daha sonrasında kendi average ratignlerini hesaplamak.
###   - Item veya user silindiğinde gerekli review kısımlarında ve ratinglerde değişiklik yapmak. 
###






###
###
###  HELPER FUNCTION.
###
###
@app.route('/account')
def redirect_to_account():
    username = session.pop('username', None)
    if username is not None:
        session['username'] = username
        
        if session['isAdmin']:
            return render_template('admin_page.html', username=username)
        else:
            return render_template('.html',username=username)

    return redirect(url_for('login'))



###
###
###  HOME PAGE.
###
###
@app.route('/', methods=['GET', 'POST'])
def index():
    # Get all items from the database.
    db = database_utils.get_database()
    collection = db['items']
    cursor = collection.find({})
    items = [item for item in cursor]
    
    if session.get('username') is None:
        return render_template('index.html',items=items ,user=None)
    
    return render_template('index.html', items=items,user=session.get('username'))




###
###
###  BASIC ITEM PAGE.
###
###

@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_page(item_id):

    database_utils.get_database()
    items = db.items
    item_data = items.find_one({'_id': ObjectId(item_id)})
    
    return render_template('item.html', item_data=item_data)




###
###
### ADMIN CAPABILITIES.
###
###


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    
    message = ""
    if request.method == "POST":
        username = request.form.get('username')
        is_admin = request.form.get('admin') == 'on'
        password = ""
        # Check if the username is already taken.   
        if database_utils.is_eligible(username):
            user_data = {
                "username": username,
                "password": bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt()),
                "avg_rating": 0,
                "reviews": [],
                "is_admin": is_admin,
            }
            
            message = "User successfully added."
            database_utils.insert_user(user_data)
            
            
    return render_template('add_user.html', message=message)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    
    
    if request.method == 'POST':
        # Get type of the item.
        item_type = request.form['item-type']
        if item_type == 'nothing':
            #Sessiona message eklenip renderlanabilir.
            return 
        
        
        #Naptım ben ya.
        if item_type == 'clothing':
            item_name = request.form['name_clothing']
            item_description = request.form['desc_clothing']
            item_price = request.form['price_clothing']
            item_seller = request.form['seller_clothing']
            item_image = request.form['image_clothing']
               
        elif item_type == 'computer_component':
            item_name = request.form['name_computer']
            item_description = request.form['desc_computer']
            item_price = request.form['price_computer']
            item_seller = request.form['seller_computer']
            item_image = request.form['image_computer'] 
        
        elif item_type == 'monitor':
            item_name = request.form['name_monitor']
            item_description = request.form['desc_monitor']
            item_price = request.form['price_monitor']
            item_seller = request.form['seller_monitor']
            item_image = request.form['image_monitor']

        elif item_type == 'snack':
            item_name = request.form['name_snack']
            item_description = request.form['desc_snack']
            item_price = request.form['price_snack']
            item_seller = request.form['seller_snack']
            item_image = request.form['image_snack']

        
        item = default_item__data(item_type, item_name, item_description, item_price, item_seller, item_image)
        
        if item_type == 'clothing':
            item["size"] = request.form['size_clothing']
            item["color"] = request.form['color_clothing']
            
        elif item_type == 'computer_component':
            item["spec"] = request.form['spec_computer']
        
        elif item_type == 'monitor':
            item["spec"] = request.form['spec_monitor']
        
        item["reviews"] = []
        
        try:
            database_utils.insert_item(item)
            message = 'Item successfully added.'
            session['message'] = message
            session['color'] = 'green'
            return redirect(url_for('index',message=message))
        except Exception as e:
            print(e)
            message = 'Item already exists.'
            session['message'] = message
            session['color'] = 'red'
            return render_template('addItem.html', message=message)
    
    
    return render_template('addItem.html')

@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    
    message = ""
    users = database_utils.get_collection_items('users')
    
    
    if request.method == 'POST':
        to_deleted_username = request.form['username']
        print(request.form)
        try:
            database_utils.remove_user(to_deleted_username)
            users = database_utils.get_collection_items('users')
            message = 'User successfully removed.'
            return render_template('remove_user.html', message=message, users=users)
        
        except Exception as e:
            message = 'Error during user removing. Nothing changed.'
            return render_template('remove_user.html', message=message, users=users)
        
    return render_template('remove_user.html', message=message, users=users)

@app.route('/remove_item', methods=['GET', 'POST'])
def remove_item():
    
    message = ""
    items = database_utils.get_collection_items('items')
    if request.method == 'POST':
        
        # Admin check.
        if session['isAdmin']:
            to_deleted_item_id = request.form['item_id']
            print(request.form)
            try:
                database_utils.remove_item(to_deleted_item_id)
                items = database_utils.get_collection_items('items')
                message = 'Item successfully removed.'
                return render_template('remove_item.html', message=message, items=items)
            
            except Exception as e:
                print(e)
                message = 'Error during item removing. Nothing changed.'
                return render_template('remove_item.html', message=message, items=items)
        
    return render_template('remove_item.html', message=message, items=items)





    
def default_item__data(item_type, item_name, item_description, item_price, item_seller, item_image):
    
    return {
        "name": item_name,
        "description": item_description,
        "price": item_price,
        "seller": item_seller,
        "image": item_image,
        "type" : item_type
    }




###
###
###    LOGIN, REGISTER, LOGOUT FUNCTIONALITIES.
###
###


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        password2 = request.form['password2']
        
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
        
        try:
            database_utils.insert_user(user_data)
            message = 'You successfully registered.'
            session['message'] = message
            session['color'] = 'green'
            return redirect(url_for('login',message=message))
        except Exception as e:
            print(e)
            message = 'Username already exists.'
            session['message'] = message
            session['color'] = 'red'
            return render_template('register.html', message=message)
        
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = session.pop('message', None)
    color = session.pop('color', None)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = db.users.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            session['isAdmin'] = user['is_admin']
            return redirect(url_for('index', user=username))
        
        else:
            message = 'Invalid username or password'
            color = 'red'
            return render_template('login.html', message=message,color=color)    
    
    return render_template('login.html', message=message,color=color)

@app.route('/logout')
def logout():
    session.clear()
    time.sleep(1.5)
    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True)