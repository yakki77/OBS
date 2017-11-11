from flask import render_template, request, jsonify, redirect, g, url_for
from flask_login import login_user, login_required, current_user, logout_user
from devobs import app, db, lm
from .models import Users


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/account-activity')
def balance():
    return render_template('account-activity.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/billpay')
def billpay():
    return render_template('billpay.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect((url_for('index')))
    else:
        return render_template('login.html')

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.before_request
def befor_reques():
    g.user = current_user

@app.route('/login-ajax', methods=['POST'])
def login_ajax():
    if request.method == 'POST':
        user = Users.query.filter_by(account_num=request.form.get('obs_account')).first()
        if user is not None:
            login_user(user)
            return jsonify(success=True,
                       data=200,
                       message="Login succeed!")
        else:
            return jsonify(success=False,
                       data=1,
                       message="Login failed! cannot find account.")
