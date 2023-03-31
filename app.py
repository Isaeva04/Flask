from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # импорт библиотеки для базы данных
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # переменная для класса базы данных

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/сontacts')
def сontacts():
    return '<h1>Contacts: </h1>' \
           '<h3>Isaevaa@tut.by</h3>'

@app.route('/posts')
def posts():
    articles=Article.query.order_by(Article.date).all()  # вывод всех записай, first() - вывести только первую запись
    return render_template("posts.html", articles=articles)

@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'ошибка'
    else:
        return render_template("create-article.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)