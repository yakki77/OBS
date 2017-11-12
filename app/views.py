#!/usr/bin/env python
# coding=utf-8
from app import app, db
import json
import os
import base64
import traceback
from flask import request
from app.models import User, Transaction, Account, CheckInfo
from sqlalchemy import or_

basedir = os.path.abspath(os.path.dirname(__file__))


def image_to_base64(file_path):
    f = open(file_path, "rb")
    base64_str=base64.b64encode(f.read())
    f.close()
    return  base64_str


@app.route("/login", methods=['POST'])
def login():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        username = request.json['username']
        password = request.json['password']
        user_info = User.query.filter_by(username=username, password=password).first()
        if user_info is not None:
            res['success'] = 1
            res['data']['ssn'] = user_info.ssn
            res['data']['username'] = user_info.username
            res['data']['firstname'] = user_info.firstname
            res['data']['lastname'] = user_info.lastname
            res['data']['email'] = user_info.email
            res['data']['phonenumber'] = user_info.phonenumber
            res['data']['birthday'] = user_info.birthday
            res['data']['security_question'] = user_info.security_question
            res['data']['security_answer'] = user_info.security_answer
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


@app.route("/saveMoneyByCheck", methods=['POST'])
def save_money_by_check():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        check_image = request.files['checkimage']
        check_image.save(basedir+"/test")
        image_base64_path = basedir + "/" + image_to_base64(basedir+"/test")
        check_image.save(image_base64_path)

        check_number = request.json["checknumber"]
        check_money = request.json["checkmoney"]
        ssn = request.json["ssn"]
        #check_date = request.form.get("checkdate")
        toaccount = request.json["account"]

        check_info = CheckInfo.query.filter_by(checknumber=check_number, money=check_money).first()
        if check_info is not None:
            account = Account.query.filter_by(ssn=ssn)
            if toaccount == account.spendingaccount:
                account.spendingbalance += int(check_money)
                check_info.imagepath = image_base64_path
                db.session.commit()
                res['success'] = 1
            elif toaccount == account.savingaccount:
                account.savingbalance += int(check_money)
                check_info.imagepath = image_base64_path
                db.session.commit()
                res['success'] = 1
            else:
                res["errorMsg"] = "The account not found"
    except Exception, e:
        res['errorMsg'] = "Save money by check error"
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/transforFound", methods=['POST'])
def transfor_found():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
       fromaccount = request.json["fromaccount"]
       toaccount = request.json["toaccount"]
       online_wallet_number = request.json["onlinewalletnumber"]
       money = int(request.json["money"])
       account_info = Account.query.filter_by(onlinewalletnumber=online_wallet_number).first()
       # if account can found
       if account_info is not None:
           # if from an to account are all in the online account
           if (account_info.spendingaccount in [toaccount, fromaccount]) and (account_info.savingaccount in [toaccount,fromaccount]):
               # if to account is spending account
               if toaccount == account_info.spendingaccount:
                    # if the balance is enough
                    if account_info.savingbalance - money > 0:
                       account_info.savingbalance -= money
                       account_info.spendingbalance += money
                       db.session.commit()
                       res['success'] = 1
                       res['data']['fromaccount_balance'] = account_info.savingbalance
                       res['data']['toaccount_balance'] = account_info.spendingbalance
                       return json.dumps(res)
                    else:
                       res["errorMsg"] = "There is not sufficient funds in your account"
                       return json.dumps(res)
               # if to account is saving account
               elif toaccount == account_info.savingaccount:
                    if account_info.spendingbalance - money > 0:
                       account_info.spendingbalance -= money
                       account_info.savingbalance += money
                       db.session.commit()
                       res['success'] = 1
                       res['data']['fromaccount_balance'] = account_info.spendingbalance
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
        res['errorMsg'] = "Transfor found error"
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/paybill", methods=['POST'])
def pay_bill():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        fromaccount = request.json["fromaccount"]
        toaccount = request.json["toaccount"]
        money = int(request.json["money"])
        # only spending account can pay bill
        fromaccount_info = Account.query.filter_by(spendingaccount=fromaccount).first()
        # check if to account is right
        toaccount_info = db.session.query(Account).filter(or_(Account.spendingaccount==toaccount, Account.savingaccount==toaccount)).first()
        # if the accounts are all right
        if fromaccount_info is not None and toaccount_info is not None:
            # if from account's balance is enough
            if fromaccount_info.spendingbalance - money > 0:
                fromaccount_info.spendingbalance -= money
                # check the to account type(spending or saving)
                if toaccount_info.spendingaccount == toaccount:
                    toaccount_info.spendingbalance += money
                elif toaccount_info.savingaccount == toaccount:
                    toaccount_info.savingbalance += money
                # update
                db.session.commit()
                res['success'] = 1
                res['data']['fromaccount_balance'] = fromaccount_info.spendingbalance
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

