from flask_sqlalchemy import SQLAlchemy
from flask import Flask,redirect,url_for,render_template,request,session,flash

app=Flask(__name__)
app.secret_key='just'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.sqlite3'
db=SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"
def view():
    users = User.query.all()
    result = "<h2>Users:</h2>"
    for u in users:
        result += f"<p>{u.id}. {u.name}</p>"
    return result
view()