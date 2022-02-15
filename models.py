from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
#definiendo los modelos
class NovelaModel(db.Model):
    __tablename__ = 'books'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    author = db.Column(db.String(80))
 
    def __init__(self, name, author):
        self.name = name
        self.author = author 
     
    def json(self):
        return {"name":self.name, "author":self.author}

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
