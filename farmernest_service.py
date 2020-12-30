from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'farmernest'
app.config[
    'MONGO_URI'] = 'mongodb+srv://portalappuser:admin123@cluster0.89wan.mongodb.net/farmernest?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true'

mongo = PyMongo(app)


@app.route('/')
def nativelang():
    return render_template('nativelang.html')


@app.route('/index')
def index():
    if 'username' in session:
        if session['role'] == 'farmer':
            return redirect(url_for('dashboardf'));
        else:
            return redirect(url_for('dashboardo'));

    return render_template('index.html')


@app.route('/dashboardf')
def dashboardf():
    if 'username' in session:
        return render_template('dashboard_farmer.html');
    return render_template('index.html')



@app.route('/dashboardo')
def dashboardo():
    if 'username' in session:
        return render_template('dashboard_other.html');
    return render_template('index.html')

@app.route('/orderssu')
def orderssu():
    if 'username' in session:
        return render_template('orders_summary.html');
    return render_template('index.html')

@app.route('/support')
def support():
    if 'username' in session:
        return render_template('support.html');
    return render_template('index.html')

@app.route('/notifications')
def notifications():
    if 'username' in session:
        return render_template('notifications.html');
    return render_template('index.html')

@app.route('/neworder')
def neworder():
    if 'username' in session:
        return render_template('newOrder.html');
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    print(request.form['role']);
    login_user = users.find_one({'username': request.form['username'], 'role': request.form['role']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user[
            'password'].encode('utf-8'):
            session['username'] = request.form['username']
            session['role'] = request.form['role']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username'], 'role': request.form['role']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username': request.form['username'], 'password': hashpass, 'role': request.form['role']})
            session['username'] = request.form['username']
            session['role'] = request.form['role']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
