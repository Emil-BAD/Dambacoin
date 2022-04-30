from flask import Flask, url_for, request, render_template, redirect, abort, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms_python.loginform import LoginForm
from forms_python.regform import RegForm
from forms_python.donate_form import DonateForm
from data.users import User
import requests
from cloudipsp import Api, Checkout
from sqlalchemy import desc
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/users.db")


@app.route('/donate', methods=['GET', 'POST'])
def donate(): # страница доната
    form = DonateForm()
    if form.validate_on_submit(): # API платёжной системы
        num = int(request.form['summ'])
        api = Api(merchant_id=1396424,
                  secret_key='test')
        checkout = Checkout(api=api)
        data = {
            "currency": "RUB",
            f"amount": str(num) + "00"
        }
        url = checkout.url(data).get('checkout_url')
        print(url)

        return redirect(url)
    return render_template('О-нас.html', form=form)


@app.route('/toplist')
def toplist(): # страница с 10-ми людьми с наибольшим кол-вом коинов
    db_sess = db_session.create_session()
    users = db_sess.query(User).order_by(desc(User.coins))
    count = 0
    num = 1
    res = list()
    for i in users:
        res.append([num, i.name, i.coins, i.one_click, i.one_sec])
        count += 1
        num += 1
        if count == 10:
            break
    return render_template("Контакты.html", users=res)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/pass_val', methods=['OPTIONS'])
@login_required
def pass_val(): # страница принятие данных от JS с помощью ajax и их запись в БД
    string = request.args.get('value')
    id = string.split(',')[0]
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.coins = string.split(',')[1]
    user.one_click = string.split(',')[2]
    user.one_sec = string.split(',')[3]
    user.upgrade_click1 = string.split(',')[4]
    user.upgrade_click2 = string.split(',')[5]
    user.upgrade_sec1 = string.split(',')[6]
    user.upgrade_sec2 = string.split(',')[7]
    db_sess.commit()
    return id


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/click/<int:id>', methods=['GET', 'POST'])
@login_required
def click(id): # страница главного кликера
    if current_user.is_authenticated and request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.id == current_user.id and User.email == current_user.email and User.name == current_user.name).first()
        param = {}
        param['coins'] = int(user.coins)
        param['click_sec'] = int(user.one_sec)
        param['one_click'] = int(user.one_click)
        param['id'] = int(user.id)
        param['upgrade_click1'] = int(user.upgrade_click1)
        param['upgrade_click2'] = int(user.upgrade_click2)
        param['upgrade_sec1'] = int(user.upgrade_sec1)
        param['upgrade_sec2'] = int(user.upgrade_sec2)
        param['one_click'] = int(user.one_click)
        param['sec_click'] = int(user.one_sec)
    return render_template('Страница-1.html', **param)


@app.route('/reg', methods=['GET', 'POST'])
def reg(): # страница регистрации
    form = RegForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit(): # проверка нажатия кнопки в html
        if len(request.form['password']) < 8:
            return render_template("Регистрация.html", form=form, message='Длинна пароля меньше 8 символов')
        if request.form['password'] != request.form['repeatpassword']:
            return render_template("Регистрация.html", form=form, message='Пароли не совпадают')
        for user in db_sess.query(User).all():
            if user.email != request.form['email']:
                continue
            else:
                return render_template("Регистрация.html", form=form, message='Такая эл.почта уже зарегистрирована')
        user = User() # отправка в БД
        user.name = request.form['username']
        user.email = request.form['email']
        user.set_password(request.form['password']) 
        user.coins = 0
        user.one_click = 1
        user.one_sec = 0
        user.upgrade_click1 = 0
        user.upgrade_click2 = 0
        user.upgrade_sec1 = 0
        user.upgrade_sec2 = 0
        db_sess.add(user)
        db_sess.commit()
        return redirect(url_for('login'))
    return render_template("Регистрация.html", form=form, message='')


@app.route('/login', methods=['GET', 'POST'])
def login(): # страница входа
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(f'/click/{user.id}')
        return render_template('Вход.html', form=form, message='Неверные эл.почта или пароль')
    return render_template('Вход.html', form=form, message=' ')


@app.route('/main', methods=['GET', 'POST'])
def main():  # страница главная
    response = requests.get('https://api.chucknorris.io/jokes/random').json()  # получение json с API Чака Норисса
    chuck_norris_joke = str(response['value'])
    return render_template("Главная.html", joke=chuck_norris_joke)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)
