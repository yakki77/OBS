from flask import render_template, request, jsonify
from flask_login import login_user, login_required
from devobs import app, db, lm
from .models import Users

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
    else:
        return render_template('login.html')