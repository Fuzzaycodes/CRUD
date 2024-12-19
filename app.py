from flask import Flask, render_template, redirect, request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#data model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

 #to retur data   
def __repr__(self):
        return f'<Task {self.id}'


@app.route("/",methods=["POST","GET"])#to enable sending and receiving data
@app.route("/home")

def home():
#adding a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"   
#to  see all tasks
    else:
        tasks = MyTask.query.order_by(MyTask.date_created).all()
        return render_template('index.html', tasks=tasks)

#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

#update an item
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return "HOME"




if __name__ == "__main__":
    with app.app_context():
        db.create_all()#creates instance file with db
    app.run(debug=True)
