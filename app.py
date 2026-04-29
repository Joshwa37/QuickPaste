from flask import Flask,redirect,url_for,render_template,request,session,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key='just'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market1.sqlite3'
db=SQLAlchemy(app)

class user(db.Model):
    email=db.Column(db.String(100),primary_key=True)
    password=db.Column(db.String(100))
    content=db.Column(db.String())

    def __init__(self,email,password,content):
        self.email=email
        self.password=password
        self.content=content

class defaultc(db.Model):
    content=db.Column(db.String())
    path=db.Column(db.String(),primary_key=True)

    def __init__(self,content,path):
        self.content=content
        self.path=path


@app.route("/")
def default1():
    return redirect(url_for('home'))
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        email1=request.form['email']
        password1=request.form['password']
        content1=request.form['content']
        newuser=user(email=email1,password=password1,content=content1)
        db.session.add(newuser)
        db.session.commit()
        use=user.query.filter_by(email=email1).first()
        return render_template('use.html',content=content1)
        
    return render_template('register.html')

@app.route('/view')
def view():
    users = user.query.all()
    result = "<h2>Users:</h2>"
    for u in users:
        result += f"<p>{u.email}. {u.password}</p>"
    return result

@app.route('/login',methods=['POST','GET'])
def login():
    users = user.query.all()
    if request.method=='POST':
        email1=request.form['email']
        password1=request.form['password']
        for u in users:
            if(u.email==email1):
                if(u.password==password1):
                    flash('success', 'success')
                    return use(u.email,u.content)
                else:
                    flash('Invalid password', 'error')
                    return redirect("/login")
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/<path:email>')
def use(email,content):
    return render_template('use.html',content=content)

@app.route('/delete',methods=['POST','GET'])
def delete():
    users = user.query.all()
    if request.method=='POST':
        email1=request.form['email']
        password1=request.form['password']
        for u in users:
            if(u.email==email1):
                if(u.password==password1):
                    u.query.filter_by(email=email1).delete()
                    db.session.commit()
                    flash('success', 'success')
                    return redirect('/login')
                else:
                    flash('Invalid password', 'error')
        flash('Invalid username or password', 'error')
    return render_template('delete.html')
@app.route('/default',methods=['POST','GET'])
def default():
    if request.method=='POST':
        path=request.form['path']
        content1=request.form['content']
        newuser=defaultc(path=path,content=content1)
        db.session.add(newuser)
        db.session.commit()
    return render_template('default.html')

@app.route("/<name>")
def ran(name):
    users = defaultc.query.all()
    for u in users:
        if(u.path==name):
            return render_template('rab.html',content=u.content)
    return render_template("rab.html")

      
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

