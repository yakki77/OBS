#!/usr/bin/env python
# coding=utf-8
from app import app, db
import json
import os
import base64
import traceback
from flask import Flask, request, render_template, redirect, url_for, session
from app.models import User, Transaction, Account, CheckInfo

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
        username = request.form.get('username')
        password = request.form.get('password')
        user_info = User.query.filter_by(username=username, password=password).first()
        if user_info != None:
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
            res['errorMsg'] = "username or password error"
    except Exception, e:
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/register", methods=['POST'])
def register():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        ssn = request.form.get("ssn")
        online_wallet_number = request.form.get('onlinewalletnumber')
        pin_password = request.form.get("pinpassword")
        # search if it has
        ssn_account = Account.query.filter_by(ssn=ssn).first()
        print "ssn account: ", ssn_account
        if ssn_account != None and ssn_account.onlinewalletnumber == online_wallet_number and ssn_account.pinpassword == pin_password:
            # add in user table
            print "check ssn account success"
            db.session.add(User(ssn=ssn))
            db.session.commit()
            print "add user success"
            res['success'] = 1
            res['data']['ssn'] = ssn
            res['data']['online_wallet_number'] = online_wallet_number

    except Exception, e:
        res['errorMsg'] = "register error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/updatePersonInfo", methods=['POST'])
def update_personal_info():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        ssn = request.form.get("ssn")
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        email = request.form.get("email")
        phonenumber = request.form.get("phonenumber")
        birthday = request.form.get("birthday")
        security_question = request.form.get("securityquestion")
        security_answer = request.form.get("securityanswer")

        # update info
        user = User.query.filter_by(ssn=ssn).first()
        if user != None:
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
        res['errorMsg'] = "update info error"
        print traceback.format_exc()

    return json.dumps(res)

@app.route("/getUserInfo", methods=['GET'])
def get_user_info():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        user_info = User.query.filter_by(username=username, password=password).first()
        if user_info != None:
            res['data']['ssn'] = user_info.ssn
            res['data']['username'] = user_info.username
            res['data']['email'] = user_info.email
            res['data']['firstname'] = user_info.firstname
            res['data']['lastname'] = user_info.lastname
            res['data']['phonenumber'] = user_info.phonenumber
            res['data']['birthday'] = user_info.birthday
            res['data']['security_question'] = user_info.security_question
            res['data']['security_answer'] = user_info.security_answer
            res['success'] = 1
    except Exception, e:
        print traceback.format_exc()
        res['errorMsg'] = "get user info error"

    return json.dumps(res)


@app.route("/saveMoneyByCheck", methods=['POST'])
def save_money_by_check():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
        check_image = request.files['checkimage']
        check_image.save(basedir+"/test")
        image_base64_path = basedir + "/" + image_to_base64(basedir+"/test")
        check_image.save(image_base64_path)

        check_number = request.form.get("checknumber")
        check_money = request.form.get("checkmoney")
        ssn = request.form.get("ssn")
        check_date = request.form.get("checkdate")
        toaccount = request.form.get("account")

        check_info = CheckInfo.query.filter_by(checknumber=check_number, money=check_money).first()
        if check_info != None:
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
        print traceback.format_exc()

    return json.dumps(res)


@app.route("/transforFound", methods=['POST'])
def transfor_found():
    res = {"errorMsg":"", "data":{}, "success": 0}
    try:
       fromaccount = request.form.get("fromaccount")
       toaccount = request.form.get("toaccount")
       online_wallet_number = request.form.get("onlinewalletnumber")
       money = int(request.form.get("money"))
       account_info = Account.query.filter_by(onlinewalletnumber=online_wallet_number).first()
       # if account can found
       print type(account_info.savingbalance)
       if account_info != None:
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
                       res['data']['from_account_balance'] = account_info.savingbalance
                       res['data']['to_account_balance'] = account_info.spendingbalance
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
                       res['data']['from_account_balance'] = account_info.spendingbalance
                       res['data']['to_account_balance'] =  account_info.savingbalance
                       return json.dumps(res)
                    else:
                       res["errorMsg"] = "There is not sufficient funds in your account"
                       return json.dumps(res)
           else:
               res["errorMsg"] = "the accounts are not in your online wallet"
               return json.dumps(res)
       # if account not fount
       else:
           res['errorMsg'] = "the online wallet number error"
           return json.dumps(res)

    except Exception, e:
       print traceback.format_exc()

    return json.dumps(res)


@app.route("/paybill", methods=['POST'])
def pay_bill():
    res = {"errorMsg":"", "data":{}, "success": 0}
    pass
    # try:
    #     fromaccount = request.form.get("fromaccount")
    #     toaccount = request.form.get("toaccount")
    #     money = request.form.get("money")
    #     fromaccount_info = Account.query.filter_by(spendingaccount=fromaccount)
    #     toaccount_info = Account.query.filter(or_(fromaccount))
    #
    #
    # except Exception, e:
    #     pass
    #
    # return json.dumps(res)



