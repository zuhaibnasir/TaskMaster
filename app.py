from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    content= db.Column(db.String, nullable=False)
    created= db.Column(db.DateTime, default = datetime.utcnow)
    completed= db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        new_task = Task(content = request.form['content'])
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except :
            return "An exception occurred while adding this task."
    else:
        tasks = Task.query.order_by(Task.created).all()
        return render_template("index.html", tasks = tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except expression as identifier:
        return "An exception occurred while deleting this task."


@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id):
    task_to_update = Task.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task_to_update.content = request.form['content']
            db.session.commit()
            return redirect("/")
        except :
            return "An exception occurred while updating this task."
    else:        
        return render_template("update.html", task = task_to_update)


if __name__ == "__main__":
    app.run(debug = True)