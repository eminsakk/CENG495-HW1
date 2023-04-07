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
authenticated_user,isAdmin = None,None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global authenticated_user
    global isAdmin
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

@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    return render_template('test.html', username=authenticated_user)


@app.route('/account')
def redirect_to_account():
    username = session.pop('username', None)
    if username is not None:
        if isAdmin:
            return render_template('admin_page.html', username=authenticated_user)
        else:
            return render_template('admin_page.html',username=authenticated_user)
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get items in the database.
    
    user_auth = request.args.get('user')
    db = database_utils.get_database()
    collection = db['items']
    cursor = collection.find({})
    items = [item for item in cursor]
    
    user_collection = db['users']
    cursor = user_collection.find({})
    users = [user for user in cursor]
    # Render the index.html template with the items as a context variable.
    # return render_template('remove_user.html',users=users)
    return render_template('index.html', items=items,user=user_auth)


def default_item__data(item_type, item_name, item_description, item_price, item_seller, item_image):
    
    return {
        "name": item_name,
        "description": item_description,
        "price": item_price,
        "seller": item_seller,
        "image": item_image,
        "type" : item_type
    }



@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    
    
    message = ""
    if request.method == "POST":
        username = request.form.get('username')
        avg_rating = request.form.get('average-rating')
        reviews = request.form.get('reviews')
        is_admin = request.form.get('admin') == 'on'
        
        # Check if the username is already taken.
    
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




@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_page(item_id):

    database_utils.get_database()
    items = db.items
    item_data = items.find_one({'_id': ObjectId(item_id)})
    
    reviews = item_data['reviews']
        
    
    return render_template('item.html', item_data=item_data)
    
    
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


@app.route('/logout')
def logout():
    global authenticated_user,isAdmin
    authenticated_user,isAdmin = None,None
    session.pop('username', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)