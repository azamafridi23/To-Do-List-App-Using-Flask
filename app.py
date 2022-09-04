# from urllib import request
from flask import Flask,render_template,request,redirect
# render_template is used to render/implement templates on the site. It is used with return keyword
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    # whenever the object is called then this will be printed.
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/",methods=['GET','POST'])
def add():
    if request.method=='POST':
        title=request.form['title'] # done by using name attribute in the <!-- FROM-S -->
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "This is products page"


@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title'] # done by using name attribute in the <!-- FROM-S -->
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    print(f'{sno} DELETED !!')
    return redirect("/") # '/' means ke back to main page

if __name__=="__main__":
    app.run(debug=True,port=8000)
