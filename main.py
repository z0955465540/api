# from api_webserver.resources import account
import flask
from flask import request,jsonify
from flask.wrappers import Response
from flask_restful import Api,Resource
import pymysql
from resources.user import Users,User
from resources.account import Accounts,Account


app = flask.Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)
api.add_resource(Users,'/users')#靜態IP
api.add_resource(User,'/user/<id>')
api.add_resource(Accounts,'/bank-accounts')#靜態IP
api.add_resource(Account,'/bank-account/<id>')
#api.add_resource(Users,'/use/users/<id>')#動態IP

@app.route('/',methods = ['GET'])
def home():
    return 'hello'

#增加驗證授權
@app.before_request
def auth():
    token = request.headers.get('auth')
    if token == '567':
        pass
    else:
        response = {'msg':'invalid token'}
        return response,401

#隱藏一長串錯誤碼
@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if(type(error).__name__ == 'NotFound'):
        status_code = 404
    else:
        pass
    return {'msg':type(error).__name__},status_code

#存款
@app.route('/account/<account_number>/deposit',methods = ['POST'])
def deposit(account_number):
    db,cursor,account = get_account(account_number)
    money = request.values['money']
    balance = account['balance']+ int(money)
    sql = """
    Update API.Accounts Set balance = {}
    where account_number = '{}'
    """.format(balance,account_number)
    cursor.execute(sql)
    db.commit()
    db.close()
    response = {
        'result':True
    }
    return jsonify(response)

#提款
@app.route('/account/<account_number>/withdraw',methods = ['POST'])
def withdraw(account_number):
    db,cursor,account = get_account(account_number)
    money = request.values['money']
    balance = account['balance']- int(money)
    if balance < 0 :
        response = {
            'result':False,
            'mag':'餘額不足'
        }
        code = 400
    else:
        sql = """
        Update API.Accounts Set balance = {}
        where account_number = '{}'
        """.format(balance,account_number)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        code = 200
    return jsonify(response),code

def get_account(account_number):
    db = pymysql.connect('192.168.56.114','porter','porter','API')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        Select * From API.Accounts
        where account_number = '{}'
    """.format(account_number)
    cursor.execute(sql)
    return db,cursor,cursor.fetchone()

if __name__ == '__main__':
    app.run(port = 5555)