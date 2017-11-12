#!/usr/bin/env python
# coding=utf-8
from app import app, db
import json
import os
import traceback
import datetime
from flask import request
from app.models import User, Transaction, Account, CheckInfo
from sqlalchemy import or_

basedir = os.path.abspath(os.path.dirname(__file__))


@app.route("/login", methods=['POST'])
def login():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        username = request.json['username']
        password = request.json['password']
        user_info = User.query.filter_by(username=username, password=password).first()
        if user_info is not None:
            account_info = Account.query.filter_by(ssn=user_info.ssn).first()
            res['success'] = 1
            res['data']['checkingaccount'] = account_info.checkingaccount
            res['data']['savingaccount'] = account_info.savingaccount
            res['data']['checkingbalance'] = account_info.checkingbalance
            res['data']['savingbalance'] = account_info.savingbalance
            return json.dumps(res)
        else:
            res['errorMsg'] = "Username or password error"
    except Exception, e:
        res['errorMsg'] = "Login error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/register", methods=['POST'])
def register():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        ssn = request.json["ssn"]
        online_wallet_number = request.json['onlinewalletnumber']
        pin_password = request.json["pinpassword"]
        # search if it has
        ssn_account = Account.query.filter_by(ssn=ssn).first()
        if ssn_account is not None and ssn_account.onlinewalletnumber == online_wallet_number and ssn_account.pinpassword == pin_password:
            # add in user table
            db.session.add(User(ssn=ssn))
            db.session.commit()
            res['success'] = 1
            res['data']['ssn'] = ssn
            res['data']['onlinewalletnumber'] = online_wallet_number

    except Exception, e:
        res['errorMsg'] = "Register error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/updateUserInfo", methods=['POST'])
def update_personal_info():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        ssn = request.json["ssn"]
        username = request.json["username"]
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        password = request.json["password"]
        email = request.json["email"]
        phonenumber = request.json["phonenumber"]
        birthday = request.json["birthday"]
        security_question = request.json["securityquestion"]
        security_answer = request.json["securityanswer"]

        # update info
        user = User.query.filter_by(ssn=ssn).first()
        if user is not None:
            user.username = username
            user.firstname = firstname
            user.lastname = lastname
            user.password = password
            user.email = email
            user.phonenumber = phonenumber
            user.birthday = birthday
            user.security_question = security_question
            user.security_answer = security_answer
            db.session.commit()
            res['success'] = 1

    except Exception, e:
        res['errorMsg'] = "Update info error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/getUserInfo", methods=['GET'])
def get_user_info():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        username = request.args.get("username")
        print request.args
        user_info = User.query.filter_by(username=username).first()
        print user_info
        if user_info is not None:
            res['data']['ssn'] = user_info.ssn
            res['data']['username'] = user_info.username
            res['data']['email'] = user_info.email
            res['data']['firstname'] = user_info.firstname
            res['data']['lastname'] = user_info.lastname
            res['data']['phonenumber'] = user_info.phonenumber
            res['data']['birthday'] = user_info.birthday
            res['data']['securityquestion'] = user_info.security_question
            res['data']['securityanswer'] = user_info.security_answer
            res['success'] = 1
    except Exception, e:
        res['errorMsg'] = "Get user info error"
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/depositByCheck", methods=['POST'])
def deposit_by_check():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        check_number = request.form.get("checknumber")
        check_amount = request.form.get("checkmoney")
        check_image_front = request.files['checkfrontimage']
        front_image_path = basedir+"/checkImage/" + check_number + "-front.jpg"
        check_image_front.save(front_image_path)
        # front_image_base64_path = basedir + "/" + image_to_base64(basedir+"/testfront")
        # check_image_front.save(front_image_base64_path)

        check_image_back = request.files['checkbackimage']
        back_image_path = basedir+"/checkImage/" + check_number + "-back.jpg"
        check_image_back.save(back_image_path)
        # back_image_base64_path = basedir + "/" + image_to_base64(basedir+"/testback")
        # check_image_back.save(back_image_base64_path)
        #check_date = request.form.get("checkdate")
        toaccount = request.form.get("account")

        check_info = CheckInfo.query.filter_by(checknumber=check_number, amount=check_amount).first()
        if check_info is not None:
            account = db.session.query(Account).filter(or_(Account.checkingaccount==toaccount, Account.savingaccount==toaccount)).first()
            if toaccount == account.checkingaccount:
                account.checkingbalance += int(check_amount)
                check_info.imagepath = front_image_path + ":" + back_image_path
                db.session.add(Transaction(time=datetime.date.today(), fromaccount="check:"+check_number, toaccount=toaccount, amount=check_amount))
                db.session.commit()
                res['success'] = 1

            elif toaccount == account.savingaccount:
                account.savingbalance += int(check_amount)
                check_info.imagepath = front_image_path + ":" + back_image_path
                db.session.add(Transaction(time=datetime.date.today(), fromaccount="check:"+check_number, toaccount=toaccount, amount=check_amount))
                db.session.commit()
                res['success'] = 1
            else:
                res["errorMsg"] = "The account is not found"
        else:
            res["errorMsg"] = "The check is not found"
    except Exception, e:
        res['errorMsg'] = "Save amount by check error"
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/transferFund", methods=['POST'])
def transfer_fund():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
       fromaccount = request.json["fromaccount"]
       toaccount = request.json["toaccount"]
       online_wallet_number = request.json["onlinewalletnumber"]
       amount = int(request.json["money"])
       account_info = Account.query.filter_by(onlinewalletnumber=online_wallet_number).first()
       # if account can find
       if account_info is not None:
           # if from an to account are all in the online account
           if (account_info.checkingaccount in [toaccount, fromaccount]) and (account_info.savingaccount in [toaccount,fromaccount]):
               # if to account is checking account
               if toaccount == account_info.checkingaccount:
                    # if the balance is enough
                    if account_info.savingbalance - amount > 0:
                       account_info.savingbalance -= amount
                       account_info.checkingbalance += amount
                       db.session.add(Transaction(time=datetime.date.today(), fromaccount=fromaccount, toaccount=toaccount, amount=amount))
                       db.session.commit()
                       res['success'] = 1
                       res['data']['fromaccount_balance'] = account_info.savingbalance
                       res['data']['toaccount_balance'] = account_info.checkingbalance
                       return json.dumps(res)
                    else:
                       res["errorMsg"] = "There is not sufficient funds in your account"
                       return json.dumps(res)
               # if to account is saving account
               elif toaccount == account_info.savingaccount:
                    if account_info.checkingbalance - amount > 0:
                       account_info.checkingbalance -= amount
                       account_info.savingbalance += amount
                       db.session.add(Transaction(time=datetime.date.today(), fromaccount=fromaccount, toaccount=toaccount, amount=amount))
                       db.session.commit()
                       res['success'] = 1
                       res['data']['fromaccount_balance'] = account_info.checkingbalance
                       res['data']['toaccount_balance'] = account_info.savingbalance
                       return json.dumps(res)
                    else:
                       res["errorMsg"] = "There is not sufficient funds in your account"
                       return json.dumps(res)
           else:
               res["errorMsg"] = "The accounts are not in your online wallet"
               return json.dumps(res)
       # if account not fount
       else:
           res['errorMsg'] = "The online wallet number error"
           return json.dumps(res)

    except Exception, e:
        res['errorMsg'] = "Transfer fund error"
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/paybill", methods=['POST'])
def pay_bill():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        fromaccount = request.json["fromaccount"]
        toaccount = request.json["toaccount"]
        amount = int(request.json["money"])
        # only checking account can pay bill
        fromaccount_info = Account.query.filter_by(checkingaccount=fromaccount).first()
        # check if to account is right
        toaccount_info = db.session.query(Account).filter(or_(Account.checkingaccount==toaccount, Account.savingaccount==toaccount)).first()
        # if the accounts are all right
        if fromaccount_info is not None and toaccount_info is not None:
            # if from account's balance is enough
            if fromaccount_info.checkingbalance - amount > 0:
                fromaccount_info.checkingbalance -= amount
                # check the to account type(checking or saving)
                if toaccount_info.checkingaccount == toaccount:
                    toaccount_info.checkingbalance += amount
                elif toaccount_info.savingaccount == toaccount:
                    toaccount_info.savingbalance += amount
                # update
                db.session.add(Transaction(time=datetime.date.today(), fromaccount=fromaccount, toaccount=toaccount, amount=amount))
                db.session.commit()
                res['success'] = 1
                res['data']['fromaccount_balance'] = fromaccount_info.checkingbalance
                return json.dumps(res)
            else:
                res["errorMsg"] = "There is not sufficient funds in your account"
                return json.dumps(res)
        else:
            # if from account is not right
            if fromaccount_info is None:
                res['errorMsg'] = "From account error, check your account"
            # if to account is not right
            elif toaccount_info is None:
                res["errorMsg"] = "To account error, check your account"
            return json.dumps(res)

    except Exception, e:
        res['errorMsg'] = "Pay bill error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/accountActivity", methods=['POST'])
def account_activity():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        account_number = request.json['account_number']
        user = request.json['user']
        account_info = db.session.query(Account).filter(or_(Account.checkingaccount==account_number, Account.savingaccount==account_number)).first()
        if account_info is not None:
            if account_number == account_info.checkingaccount:
                res['data']['account_balance'] = account_info.checkingbalance
            elif account_number == account_info.savingaccount:
                res['data']['account_balance'] = account_info.savingbalance
        else:
            res['errorMsg'] = "Account number is not right"
            return json.dumps(res)

        transaction_info = db.session.query(Transaction).filter(or_(Transaction.fromaccount==account_number, Transaction.toaccount==account_number)).all()
        history = {}
        for info in transaction_info:
            if not history.has_key(info.time):
                history[info.time] = []
                if info.fromaccount == account_number:
                    history[info.time].append({"action": "out", "toaccount": info.toaccount, "money": info.amount})
                elif info.toaccount == account_number:
                    history[info.time].append({"action": "in", "fromaccount": info.fromaccount, "money": info.amount})
            else:
                if info.fromaccount == account_number:
                    history[info.time].append({"action": "out", "toaccount": info.toaccount, "money": info.amount})
                elif info.toaccount == account_number:
                    history[info.time].append({"action": "in", "fromaccount": info.fromaccount, "money": info.amount})

        res_history = []
        for time in history:
            res_history_tmp = {time: history[time]}
            res_history.append(res_history_tmp)
        res['data']['account_activity'] = res_history
        res['success'] = 1

    except Exception, e:
        res['errorMsg'] = "Get transaction history error"
        print traceback.format_exc()

    return json.dumps(res)


