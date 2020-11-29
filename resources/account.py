from flask.wrappers import Response
from flask_restful import Resource,reqparse
from flask import jsonify
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    #顯示SQL的DATABASE全部資料
    def get(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """Select * From API.Accounts"""
        cursor.execute(sql)
        accounts = cursor.fetchall()
        db.close()
        response = {
            'data':accounts
        }
        return jsonify(response)
    #使用POSTMAN新增資料進SQL
    def post(self):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number']
        }
        sql = """Insert into API.Accounts(balance,account_number)values('{}','{}')
                """.format(account['balance'],account['account_number'])
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)

class Account(Resource):
    #初始設定SQL
    def db_init(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    #指定收尋ID資料  ex.(http://127.0.0.1:5555/account/1(id))
    def get(self,id):
        db,cursor = self.db_init()
        sql = """Select * From API.Accounts
                where id = '{}'""".format(id)
        cursor.execute(sql)
        account = cursor.fetchall()
        db.close()
        response = {
            'data':account
        }
        return jsonify(response)
    #單筆修改SQL的內容
    def patch(self,id):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number']
        }
        query = []
    
        for key, value in account.items():
            if value != None:
                query.append(key + ' = ' + "' {} '".format(value))
        query = ','.join(query)
        sql = """ Update API.accounts Set {} where id = "{}" """.format(query, id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)
    #單筆刪除SQL的內容
    def delete(self,id):
        db,cursor = self.db_init()
        sql = """Delete From API.Accounts
                where id = '{}'""".format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)
    #軟刪除SQL的內容
    def delete(self,id):
        db,cursor = self.db_init()
        sql = """Update API.accounts Set deleted = True
                where id = '{}'""".format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)
    #指定收尋ID資料+把軟刪除資料隱藏  ex.(http://127.0.0.1:5555/account/1(id))
    def get(self,id):
        db,cursor = self.db_init()
        sql = """Select * From API.Accounts
                where deleted = False""".format(id)
        cursor.execute(sql)
        account = cursor.fetchall()
        db.close()
        response = {
            'data':account
        }
        return jsonify(response)
    
