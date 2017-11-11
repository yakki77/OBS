from devobs import db

class Users(db.Model):
    __tablename__ = 'obs_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_num = db.Column(db.BIGINT, unique=True, index=True)
    pwd = db.Column(db.String(64), index=True)
    test = db.Column(db.String(64))


    def __init__(self, account_num, pwd):
        self.account_num = account_num
        self.pwd = pwd

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False