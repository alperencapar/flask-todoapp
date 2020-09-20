#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application

from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/alper/Desktop/Python/3 TodoApp/todo.db'
db = SQLAlchemy(app)


#! Anasayfa
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

#! Ekleme
@app.route("/add" , methods = ["POST"])
def addTodo():
    title = request.form.get("title")   #"title" name'ine sahip input'un değerini title adlı değişkene aktardık
    newTodo = Todo(title = title, complete = False)     #yeni obje oluşturuldu, aldığımız değeri ve db'deki complete değerini girdik
    db.session.add(newTodo)                             #verdiğimiz bilgileri database'e ekledik
    db.session.commit()                                 #database'e veri ekleneceği için değişikleri ekledik
    return redirect(url_for("index"))                   #index fonksiyonunun ilişkili olduğu adrese(route) yönlendiriyoruz


#! Güncelleme
@app.route("/complete/<string:id>")
def todoComplete(id):
    
    todo = Todo.query.filter_by(id=id).first()  #db'den id ile veri çekiliyor

    todo.complete = not todo.complete   #True ise False, False ise True yap
    db.session.commit()

    return redirect(url_for("index"))


#! Silme
@app.route("/delete/<string:id>")
def todoDelete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


#? Database tablo yapısı oluştur
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all() #? Database tablosu oluştur
    app.run(debug=True)