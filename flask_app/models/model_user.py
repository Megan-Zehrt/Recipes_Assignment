#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_recipe
# model the class after the user table from our database
from flask_app import DATABASE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
   def __init__(self, data:dict):
      self.id = data['id']
      self.first_name = data['first_name']
      self.last_name = data['last_name']
      self.email = data['email']
      self.password = data['password']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']

      #Add additional columns from database here

   def info(self):
      returnStr = f"First Name = {self.first_name} || Last Name = {self.last_name} || Email = {self.email} Password = {self.password}"
      return returnStr

#CREATE
   @classmethod
   def create_one(cls, data:dict):
      query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
      print("this is the model file")
      result = connectToMySQL(DATABASE).query_db(query, data)
      print(data)
      return result
       
   # now we use the class methods to query our database 

#READ
   @classmethod
   def get_all(cls) -> list:
      query = "SELECT * FROM users;"
      #make sure to call the connectToMySQL function with the schema you are targeting

      results = connectToMySQL(DATABASE).query_db(query)
      #create an empty list to append our instances of users
      if not results:
         return []

      instance_list = []
      # iterate over the db results anad create instances of users with cls.
      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list

   @classmethod
   def get_one(cls, data):
      query = "SELECT * FROM users WHERE id = %(id)s;"
      #data = {'id': user_id}
      results = connectToMySQL(DATABASE).query_db(query, data)
      if not results:
         return []

      instance_list = []

      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list


   @classmethod
   def get_by_email(cls,data):
      query = "SELECT * FROM users WHERE email = %(email)s;"
      result = connectToMySQL(DATABASE).query_db(query,data)
      # Didn't find a matching user
      if len(result) < 1:
         return False
      return cls(result[0])


# Validators

   @staticmethod
   def validator(data: dict) -> bool:
      is_valid = True

      if(len(data['first_name']) < 2):
         flash("First Name must be more than 2 Characters in length", "err_users_first_name")
         is_valid = False

      if(len(data['last_name']) < 2):
         flash("Last Name must be more than 2 Characters in length", "err_users_last_name")
         is_valid = False

      if(len(data['email'])) == 0:
         flash("Not a good Email", "err_users_email")
         is_valid = False

      elif not EMAIL_REGEX.match(data['email']):
         flash("Invalid email address", "err_users_email")
         is_valid = False
      
      else:
         potential_user = User.get_by_email(data)
         if potential_user:
            flash("This Email already exists", "err_users_email")
            is_valid = False


      if(len(data['password']) < 8):
         flash("Not a good password", "err_users_password")
         is_valid = False

      if(len (data['confirm_password']) < 8):
         flash("Confirm Password is not Valid", "err_users_confirm_password")
         is_valid = False

      elif((data['confirm_password']) != (data['password'])):
         flash("Confirm Password must Match Password", "err_users_confirm_password")
         is_valid = False


      return is_valid
      #run through some if checks -> if if checks come out to be bad then is_valid = False

# Validators

   @staticmethod
   def validator_login(data: dict) -> bool:
      is_valid = True

      if(len(data['email'])) == 0:
         flash("Invalid Email", "err_users_loginemail")
         is_valid = False

      elif not EMAIL_REGEX.match(data['email']):
         flash("Invalid email address", "err_users_loginemail")
         is_valid = False


      if(len(data['password']) < 8):
         flash("Invalid password", "err_users_loginpassword")
         is_valid = False




      return is_valid

# SAVE
   @classmethod
   def save(cls,data):
      query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
      result = connectToMySQL(DATABASE).query_db(query, data)
      return result



