from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random


app = Flask(__name__)

# レイアウトサンプル
@app.route('/')
def sample_top():
    return render_template('index.html')

@app.route('/list')
def sample_list():
    book_list = [
        ('よく分かるPython', '佐々木 磨生', 'MCL出版', 200),
        ('LinuC 詳解', '細川 潤哉', 'MCL出版', 400),
        ('Servlet 入門', '高橋 洋平', 'ジョビ出版', 250),
        ('Flask 入門', '高橋 洋平', 'ジョビ出版', 150),
        ('よく分かるUML', '細川 潤哉', 'MCL出版', 220),
        ('Django 入門', '佐々木 磨生', '龍澤出版', 350),
    ]
    return render_template('list.html', books=book_list)

@app.route('/register')
def sample_register():
    return render_template('register.html')

@app.route('/register_exe',methods=['POST'])
def register_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    pages = request.form.get('pages')
    
    db.insert_book(title,author,publisher,pages)
    
    book_list = db.select_all_books()
    
    return render_template('list.html',books=book_list)
    
@app.route('/', methods=['POST'])
def login():
    user_name=request.form.get('username')
    password=request.form.get('password')    
    
    if db.login(user_name,password):
        session['user'] = True
        return redirect(url_for('mypage'))
    else:
        error='ユーザー名またはパスワードが違います'
        input_data={'user_name':user_name, 'password':password}
        return render_template('index.html',error=error,data=input_data)
    
@app.route('/mypage', methods=['GET'])
def mypage():
    return render_template('mypage.html')
    
if __name__ == "__main__":
    app.run(debug=True)