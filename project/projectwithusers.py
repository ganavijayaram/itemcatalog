from flask import Flask, render_template, request, redirect, url_for,jsonify,flash
from itertools import zip_longest
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setupwithusers import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import func
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

engine = create_engine('sqlite:///itemcatelogwithusers.db',connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog with users Application"



@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    # check also if access token is valid or expired, if expired then resrore
    # the access token
    stored_url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % stored_access_token)
    stored_h = httplib2.Http()
    stored_result = json.loads(stored_h.request(stored_url, 'GET')[1])

    if (stored_access_token is not None and gplus_id == stored_gplus_id and
            stored_result.get('error') is None):
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = creatUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 160px; height: 160px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print("Access Token is None")
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("In gdisconnect access token is %s" % access_token)
    print("User name is: ")
    print(login_session['username'])
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print("result is")
    print(result)

    if result['status'] == '200':
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/catelog/JSON')
def getCatalog():
    categories = session.query(Item.category_id, func.count(
        Item.category_id)).group_by(Item.category_id).all()
    Category = []
    if categories:
        for cat in categories:
            items = session.query(Item).filter_by(category_id=cat.category_id).all()
            Category.append(
                {'Item': [i.serialize for i in items], 'name': cat.category_id})
    return jsonify(Category=Category)


#@app.route('/category/JSON')
#def catelogJSON():
    #session = DBSession()
    #category = session.query(Category).all()
    #for i in category:
        #result1 += jsonify(Category=[i.serialize])
    #return result1
        #return jsonify(Category=[i.serialize])
        #itemlist = session.query(Item).filter_by(id=i.id).all()
        #return jsonify(Items=[
            #i.serialize for i in itemlist ])
    #output = []
    #for i in category:
        #itemlist = session.query(Item).filter_by(id=i.id).all()
        #output += itemlist
        #return jsonify(Items=[i.serialize for i in itemlist])

#@app.route('/category/<int:category_id>/menu/JSON')
#def categoryMenuJSON(category_id):
    #session = DBSession()
    #category = session.query(Category).filter_by(id=category_id).one()
    #items = session.query(Item).filter_by(
        #category_id=category_id).all()
    #d = dict(items)
    #output=""
    #for i in items:
        #output += items.name
    #return d
    #return jsonify(Items=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE
@app.route('/category/<int:category_id>/menu/<int:item_id>/JSON')
def ItemJSON(category_id, item_id):
    #session = DBSession()
    Itemss = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Itemss.serialize)

@app.route('/')
@app.route('/category/')
def commoncategoryMenu():
    #session = DBSession()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
    login_session['state'] = state
    category = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(12).all()
    return render_template(
        'itemmenu1.html', category=category, items=items, STATE=state)

@app.route('/category/loggedin')
def loggedincategoryMenu():
    #session = DBSession()
    if 'username' not in login_session:
        return redirect('/category')
    user_id = login_session['user_id']
    category = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(12).all()
    #save = open('details.txt','a')
    #save.write(str()+"loggedincategoryMenu")
    #save.close()
    return render_template(
        'loggedinitemmenu1.html', category=category, items=items)

@app.route('/category/<int:category_id>/')
def getItems(category_id):
    #session = DBSession()
    #output = "hey"
    #return output
    categorylist = session.query(Category).all()
    category=session.query(Category).filter_by(id=category_id).first()
    items= session.query(Item).filter_by(category_id=category_id).all()
     #check if user has logged in then render template with add item
    if login_session.get('access_token') is not None:
        #save = open('details.txt','a')
        #save.write(str(login_session.get('access_token'))+"getitemsif")
        #save.close()
        return render_template(
       'additem.html', category=category, items=items,category_id=category_id,categorylist = categorylist)
    else:
        return render_template(
        'itemenu2.html', category=category, items=items,category_id=category_id,categorylist = categorylist)

@app.route('/category/<int:category_id>/<int:item_id>/')
def getDescription(category_id,item_id):
    session = DBSession()
    #output = "hey"
    #return output
    #categorylist = session.query(Category).all()
    #category=session.query(Category).filter_by(id=category_id).first()
    #items= session.query(Item).filter_by(category_id=category_id).all()
    itemdesc = session.query(Item).filter_by(id=item_id).one()
    #output = ""
    #for i in itemdesc:
        #output += i.description
    #return output
    #save = open('detail.txt','a')
    #save.write(str(login_session.get('email')))
    #save.close()
    
    if login_session.get('email') is not None :
        x=str(login_session.get('email'))
        category = session.query(Category).filter_by(id=category_id).one()
        getuserid=session.query(User).filter_by(email=x).one()
        #save = open('detail.txt','a')
        #save.write(str(getuserid.id))
        #save.close()
        descwithoptions = session.query(Item).filter_by(id=item_id,user_id=getuserid.id).first()
        save = open('detail.txt','a')
        #save.write(descwithoptions.name+" before")
        save.close()
        if descwithoptions is not None:
            return render_template(
            'descforusers.html', listt=descwithoptions,category_id=category_id,item_id=item_id)
            
        else:
            #save = open('detail.txt','a')
            #save.write(descwithoptions.name+" else")
            #save.close()
            save = open('detail.txt','a')
            #save.write(descwithoptions+" if")
            save.close()
            return render_template(
            'itemdesc.html', listt=itemdesc)
    else:
        return render_template(
        'itemdesc.html', listt=itemdesc,category_id=category_id,item_id=item_id)

#@app.route('/category/<int:category_id>/menu')           
#def categoryMenu(category_id):
    #session = DBSession()
    #category = session.query(Category).filter_by(id=category_id).one()
    #items = session.query(Item).filter_by(category_id=category_id).all()
    #return render_template(
        #'itemmenu.html', category=category, items=items)

#@app.route('/category/<int:category_id>/new', methods=[ 'POST'])
#def newItemtemplate(category_id):
    #session = DBSession()
    #if request.method == 'POST':
        #return render_template('newitem.html', category_id=category_id)

@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newItems(category_id):
    #session = DBSession()
    if 'username' not in login_session:
        return redirect('/category')
    if request.method == 'POST':
        #save = open('detail.txt','a')
        #save.write(str(login_session['user_id']))
        #save.close()
        newItem = Item(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id,user_id=login_session['user_id'])
        
        session.add(newItem)
        session.commit()
        return redirect(url_for('commoncategoryMenu', category_id=category_id))
    else:
        save = open('detail.txt','a')
        save.write("gett method")
        save.close()
        return render_template('newitem.html', category_id=category_id)


@app.route('/category/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/category')
    #session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.description = request.form['description']
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('commoncategoryMenu', category_id = category_id))
    else:
        return render_template(
            'edititem.html', category_id=category_id, item_id=item_id, item=editedItem)


# DELETE MENU ITEM SOLUTION
@app.route('/category/<int:category_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    #session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('commoncategoryMenu', category_id=category_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'FN8VwhXdsxtif3DwRceZCpeR'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
