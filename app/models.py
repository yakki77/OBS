#!/usr/bin/env python
# coding=utf-8

from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    ssn = db.Column(db.String(80), nullable=False, server_default='', unique=True) 
    username = db.Column(db.String(80), nullable=True, server_default='', unique=True)
    firstname = db.Column(db.String(80), nullable=True, server_default='', unique=False)
    lastname = db.Column(db.String(80), nullable=True, server_default='', unique=False)
    password = db.Column(db.String(80), nullable=True, server_default='', unique=False)
    email = db.Column(db.String(80), nullable=True, server_default='', unique=True)
    phonenumber = db.Column(db.String(30), nullable=True, server_default='', unique=True)
    birthday = db.Column(db.String(80), nullable=True, server_default='', unique=False)
    security_question = db.Column(db.String(255), nullable=True, server_default='', unique=False)
    security_answer = db.Column(db.String(80), nullable=True, server_default='', unique=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Transaction(db.Model):
    transactionid = db.Column(db.String(80), nullable=False, primary_key=True, autoincrement=True) 
    time = db.Column(db.String(80), nullable=False, server_default='', unique=False)
    fromaccount = db.Column(db.String(80), nullable=False, server_default='', unique=False)
    toaccount = db.Column(db.String(80), nullable=False, server_default='', unique=False)
    fromuser = db.Column(db.String(80), nullable=False, server_default='', unique=False)
    touser = db.Column(db.String(80), nullable=False, server_default='', unique=False)
    money = db.Column(db.Integer, nullable=False, unique=False)
    def __repr__(self):
        return '<Transaction %r>' % str(self.transactionid)

class Account(db.Model):
    onlinewalletnumber = db.Column(db.String(80), nullable=False, primary_key=True) 
    ssn = db.Column(db.String(80), nullable=False, server_default='', unique=True)
    spendingaccount = db.Column(db.String(80), nullable=False, server_default='', unique=True)
    savingaccount = db.Column(db.String(80), nullable=False, server_default='', unique=True)
    spendingbalance = db.Column(db.Integer, nullable=False, unique=False)
    savingbalance = db.Column(db.Integer, nullable=False, unique=False)
    pinpassword = db.Column(db.String(80), nullable=False, server_default='', unique=False) 
    def __repr__(self):
        return '<Account %r>' % str(self.onlinewalletnumber)

     
class CheckInfo(db.Model):
    checknumber = db.Column(db.String(80), nullable=False, primary_key=True)
    money = db.Column(db.Integer, nullable=False) 
    date = db.Column(db.String(80), nullable=False) 
    imagepath = db.Column(db.String(80), nullable=True)