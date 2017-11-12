#!/usr/bin/env python
# coding=utf-8
from app import app, db
from app.models import User, Transaction, Account
if __name__ == '__main__':
    #db.drop_all()
    db.create_all()
    app.run(debug=True)
