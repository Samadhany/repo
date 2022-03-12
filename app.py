import json

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sama'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Account(db.Model):
    __tablename__ = 'ACCOUNT_DETAILS'
    acc_num = db.Column('account_num', db.Integer, primary_key=True)
    acc_type = db.Column('account_type', db.String(20))
    acc_balance = db.Column('account_balance', db.Float)
    cust_id = db.Column('cust_id', db.Integer, db.ForeignKey('CUSTOMER_DETAILS.cust_id'), nullable=False, unique=False)


class Customer(db.Model):
    __tablename__ = 'CUSTOMER_DETAILS'

    id = db.Column('cust_id', db.Integer, primary_key=True)
    name = db.Column('cust_name', db.String(50))
    gender = db.Column('cust_gender', db.String(10))
    email = db.Column('cust_email', db.String(50), unique=True)
    image = db.Column('cust_image', db.String(255), default='NA')
    acc_ref = db.relationship(Account, backref="custref", lazy=True)


db.create_all()


@app.route('/api/v1/customer')
def get_list_of_customer():
    custlist = Customer.query.all()
    custJson = []
    for cust in custlist:
        custdict = {'custmoer_name': cust.name, 'customer_gender': cust.gender, 'customer_email': cust.email}

        custJson.append(custdict)
        return json.dumps(custJson)


def validate_customer_fields(reqBody):
    errors = {}
    if not reqBody.__contains__('CUSTOMER_EMAIL'):
        errors["email"] = "Email Address Required.."

    if not reqBody.__contains__('CUSTOMER_NAME'):
        errors['name'] = "Customer Name Required"

    if not reqBody.__contains__('CUSTOMER_GENDER'):
        errors['gender'] = 'Customer Gender Type Required..'

    return errors


@app.route('/api/v1/customer', methods=['POST'])  # ....... to insert the contents/records
def save_customer():
    reqBody = request.get_json()  # apis --- another application send karnar ahe
    print(reqBody)  # every json -- bydefault dict -->but every dict-- by default json not
    if reqBody:
        custDb = Customer.query.filter(Customer.email == reqBody.get('CUSTOMER_EMAIL')).first()
        if custDb:
            return json.dumps({'ERROR': "Duplicate Email Address"})
        # deserialing here --> as my requirement..

        errors = validate_customer_fields(reqBody)
        if errors:
            return json.dumps(errors)

        cust = Customer(name=reqBody.get('CUSTOMER_NAME'),
                        email=reqBody.get('CUSTOMER_EMAIL'),
                        gender=reqBody.get('CUSTOMER_GENDER'))
        db.session.add(cust)
        db.session.commit()
        message = "Customer recorded successfully...!"
        return json.dumps({"SUCCESS": message})
    return json.dumps({"ERROR": "Invalid Details.."})


def search_customer_by_id():
    pass


def search_customer_by_name():
    pass


def search_customer_by_accountnum():
    pass


def search_customers_account_details():
    pass


@app.route('/api/v1/customer/image', methods=['POST'])
def save_customer_with_image():
    # multimediate --> request.form -- jsoncontents ---> multimediate contents -- request.files
    reqBody = request.form
    multimedia = request.files

    print('FORMDATA', reqBody)
    print('Multimedia Contents ---', multimedia)

    cust = Customer(name=reqBody.get('CUSTOMER_NAME'),
                    email=reqBody.get('CUSTOMER_EMAIL'),
                    gender=reqBody.get('CUSTOMER_GENDER'))
    if multimedia.get('CUSTOMER_DP'):
        cust.image = 'D:\\python_code\\bank_services\\resources\\{}.png'.format(reqBody.get('CUSTOMER_NAME'))
    db.session.add(cust)
    db.session.commit()
    message = "Customer recorded successfully...!"

    file = multimedia.get('CUSTOMER_DP')
    file.save('D:\\python_code\\bank_services\\resources\\{}.png'.format(reqBody.get('CUSTOMER_NAME')))
    return json.dumps({"SUCCESS": message})


@app.route('/api/v1/', methods=['GET'])
def test_sample_api():
    return "API is up and running..!"


if __name__ == '__main__':
    app.run(debug=True)
