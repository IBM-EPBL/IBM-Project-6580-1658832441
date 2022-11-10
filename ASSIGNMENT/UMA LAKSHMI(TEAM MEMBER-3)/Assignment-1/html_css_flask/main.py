from flask import *

app = Flask(__name__)

form = {"name": "", "email": "", "password": "", "gender": "", "address": "", "country": ""}


@app.route('/appForm', methods=["GET"])
def appForm():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    gender = request.args.get('gender')
    address = request.args.get('address')
    country = request.args.get('country')
    form.update({'name': name, 'email': email, 'password': password, 'gender': gender, 'address': address, 'country': country})
    return form

if __name__ == '__main__':
    app.run(debug=True)