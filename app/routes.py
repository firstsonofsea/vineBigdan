from app import app
from app import db
from app.model import Order, Kol
from app import mail
from flask import request
from flask import jsonify
from flask_mail import Message
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def send_mail(name, kol, phone=None, email=None):
    """
    :param phone: телефон
    :param email: емаил
    :param kol: кол-во коробок
    :param name: имя к кому обращаться
    :return:
    """
    text = """Новая заявка на обратную связь от {2}
Номер телефона - {0};
Email - {1};
Кол-во коробок: {2}""".format(phone, email, name,kol)


    msg = Message("Новая заявка", recipients=['bagration1998@gmail.com'])
    msg.body = text
    mail.send(msg)
    return True


@basic_auth.verify_password
def verify_password(username, password):
    f = False
    if username == "admin" and password == "ml7TpTax":
        f = True
    return f


@app.route('/token', methods=['GET'])
@basic_auth.login_required
def get_token():
    token = 'kimetottokendlyatebya'
    return jsonify({'token': token})


@token_auth.verify_token
def verify_token(token):
    if token == 'kimetottokendlyatebya':
        return True


@app.route('/', methods=['GET'])
def qwe():
    return "hello"


@app.route('/api/new', methods=['POST'])
def new():
    try:
        r = request.json
        if r['email']:
            new_info = Order(name=r['name'], phone=r['phone'], email=r['email'], kol=r['kol'])
        else:
            new_info = Order(name=r['name'], phone=r['phone'], kol=r['kol'])
        db.session.add(new_info)
        db.session.commit()
        send_mail(phone=r['phone'], email=r['email'], kol=r['kol'], name=r['name'])
        return jsonify({"status": "OK"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error",
                        "error": str(e)})


@app.route('/api/all', methods=['GET'])
def all():
    try:
        result = []
        orders = Order.query.all()
        for i in orders:
            result.append({"name": i.name,
                           "phone": i.phone,
                           "email": i.email,
                           "kol": i.kol})
        return jsonify({"status": "OK"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error",
                        "error": str(e)})


@app.route('/api/view_kol', methods=['GET'])
def view_kol():
    try:
        result = Kol.query.filter_by(id=1).kol_vo
        return jsonify({"kol": result})
    except Exception as e:
        print(e)
        return jsonify({"status": "error",
                        "error": str(e)})


@app.route('/api/update_kol', methods=['POST'])
def update_kol():
    try:
        r = request.json
        try:
            Kol.query.filter_by(id=1).update({"kol_vo": r['kol']})
        except:
            kol = Kol(kol_vo=r['rol'])
            db.session.add(kol)
        db.session.commit()
        result = Kol.query.filter_by(id=1).kol_vo
        return jsonify({"kol": result})
    except Exception as e:
        print(e)
        return jsonify({"status": "error",
                        "error": str(e)})
