from flask.wrappers import Response
from flask_restful import Resource,reqparse
from flask import jsonify,make_response
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    #顯示SQL的DATABASE全部資料
    def get(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """Select * From API.users"""
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        response = {
            'data':users
        }
        return make_response(jsonify(response),200)
    #使用POSTMAN新增資料進SQL
    def post(self):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        if arg['birth'] == None:
            return make_response(jsonify({'msg':'未填寫生日'}),400)
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note']
        }
        sql = """Insert into API.users(name,gender,birth,note)values('{}','{}','{}','{}')
                """.format(user['name'],user['gender'],user['birth'],user['note'])
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)

class User(Resource):
    #初始設定SQL
    def db_init(self):
        db = pymysql.connect('192.168.56.114','porter','porter','API')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    #指定收尋ID資料  ex.(http://127.0.0.1:5555/user/1(id))
    def get(self,id):
        db,cursor = self.db_init()
        sql = """Select * From API.users
                where id = '{}'""".format(id)
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()
        response = {
            'data':user
        }
        return jsonify(response)
    #單筆修改SQL的內容
    def patch(self,id):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note'],
        }
        query = []
    
        for key, value in user.items():
            if value != None:
                query.append(key + ' = ' + "' {} '".format(value))
        query = ','.join(query)
        sql = """ Update API.users Set {} where id = "{}" """.format(query, id)
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
        sql = """Delete From API.users
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
        sql = """Update API.users Set deleted = True
                where id = '{}'""".format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result':True
        }
        return jsonify(response)
    #指定收尋ID資料+把軟刪除資料隱藏  ex.(http://127.0.0.1:5555/user/1(id))
    def get(self,id):
        db,cursor = self.db_init()
        sql = """Select * From API.users
                where deleted = False""".format(id)
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()
        response = {
            'data':user
        }
        return jsonify(response)
    
