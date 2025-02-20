from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

class Account(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='Jungle', port=3307, database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.accounts Where id = '{}' and where deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()

        return jsonify({'data': account})
    
    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id'],
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = " + " '{}' ".format(value))
        print(query)
        query = ", ".join(query)
        sql = """
            UPDATE `api`.`accounts` SET {} WHERE (`id` = '{}');
        """.format(query, id)
        
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)
    
    def delete(self, id):
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`accounts` SET deleted = True WHERE (`id` = '{}');
        """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='Jungle', port=3307, database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self):
        db, cursor = self.db_init()
        
        sql = 'Select * From api.accounts where deleted is not True'
        

        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()

        return jsonify({'data': accounts})
    
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id'],
        }
        sql = """
            INSERT INTO `api`.`accounts` (`balance`, `account_number`, `user_id`) VALUES ('{}', '{}', '{}');
        """.format(account['balance'], account['account_number'], account['user_id'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)