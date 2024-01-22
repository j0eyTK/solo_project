from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app
from flask import flash

import re

EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    DB = 'gym_schema'
    def __init__(self,data):
        self.id = data ['id'] 
        self.name = data ['name']
        self.email = data ['email']
        self.password = data['password']
        self.lifts=[]

    @classmethod
    def create(cls,data):

        data['password'] = bcrypt.generate_password_hash(data['password'])

        query = """INSERT INTO users (name, email, password)
        VALUES (%(name)s, %(email)s, %(password)s);"""

        return connectToMySQL(cls.DB).query_db(query,data)
        

    @staticmethod
    def validate_reg(user):
        is_valid = True
        
        if User.get_by_email(user['email']):
            flash("Sorry Email Taken", "register")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", "register")
            is_valid = False

        if len(user['name']) < 5:
            flash("Name must be 5 characters", "register")
            is_valid = False

        if len(user['password']) < 10:
            flash("Password must be 10 characters or more", "register")
            is_valid = False

        if user['password'] != user['confirm']:
            flash("Passwords need to be the same", "register")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_email(cls,email):
        query = """SELECT * FROM users
                WHERE email= %(email)s;"""
        
        results = connectToMySQL(cls.DB).query_db(query, {'email':email})
        return cls(results[0]) if results else None
    

    @classmethod
    def get_by_email(cls,email):
        query = """SELECT * FROM users
                WHERE email= %(email)s;"""
        
        results = connectToMySQL(cls.DB).query_db(query, {'email':email})
        return cls(results[0]) if results else None
    

    @classmethod
    def get_by_one(cls, data):
        query = """SELECT * FROM users
            WHERE users.id = %(id)s;"""

        results = connectToMySQL(cls.DB).query_db(query, data)

        if not results:
            return None

        return cls(results[0])
    
    @classmethod
    def get_one(cls, id):
        from flask_app.models.lift import Lift
        query = """SELECT * FROM users 
        LEFT JOIN lifts ON lifts.user_id = users.id 
        WHERE users.id = %(id)s;"""

        results = connectToMySQL(cls.DB).query_db(query,{'id':id})
        if not results:
            return None
        
        user = cls(results[0])

        for row_data in results:
            if row_data['lifts.id']:
                user.lifts.append(
                    Lift({
                    "id": row_data['lift.id'],
                    "name": row_data['name'],
                    "age": row_data['age'],
                    "lift": row_data['lift'],
                    "weight": row_data['weight'],
                    "user_id" : row_data['user_id']
                    })
                )

        return user
    

    @classmethod
    def get_one_user(cls,name):
        query = """SELECT * FROM users
                WHERE first_name = %(name)s;"""
        
        return connectToMySQL(cls.DB).query_db(query,{'name':name})