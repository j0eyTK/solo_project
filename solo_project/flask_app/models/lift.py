from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models.user import User

class Lift:
    DB = 'gym_schema'
    def __init__(self,data):
        self.id = data ['id'] 
        self.name = data ['name']
        self.age = data ['age']
        self.lift = data ['lift']
        self.weight = data['weight']
        self.poster = None

        if 'users.id' in data:
            self.poster=User({
            "id":data['users.id'],
            "name":data['name'],
            "email":data['email'],
            "password":data['password'],
        })
            

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM lifts
        LEFT JOIN users 
        ON users.id = lifts.users_id
        """

        results = connectToMySQL(cls.DB).query_db(query)
        return [cls(data) for data in results]
        

    @classmethod
    def save(cls,data):
        query = """ INSERT INTO lifts (name,age,lift,weight,users_id)
            VALUES (%(name)s, %(age)s, %(lift)s, %(weight)s, %(user_id)s);"""
        result =  connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod 
    def update(cls,data):
        query ="""UPDATE lifts 
        SET name=%(name)s, age=%(age)s, lift=%(lift)s, weight=%(weight)s 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
        
    

    @classmethod
    def delete_by_id(cls, id):
        query = """DELETE from lifts
        WHERE id = %(id)s;"""

        return connectToMySQL(cls.DB).query_db(query,{"id":id})
        
    
    @classmethod
    def get_one_by_id(cls,id):
        query = """SELECT * from lifts
        LEFT JOIN users 
        ON users.id = lifts.users_id
        WHERE lifts.id = %(id)s"""

        
        results = connectToMySQL(cls.DB).query_db(query,{"id" :id})
        if not results:
            return None
        return cls(results[0])
        
    @staticmethod
    def validate_lift(lift):
        is_valid = True

        if len(lift['name']) < 3:
            flash("Name must be 5 characters","create")
            is_valid = False

        if len(lift['age']) == 0:
            flash("Must have an age","create")
            is_valid = False

        if len(lift['lift']) == 0:
            flash("Which exercise did you do?","create")
            is_valid = False

        if len(lift['weight']) == 0:
            flash("How much weight did you move?","create")
            is_valid = False 


        return is_valid