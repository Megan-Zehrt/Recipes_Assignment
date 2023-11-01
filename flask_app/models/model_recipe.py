#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user
# model the class after the user table from our database
from flask_app import DATABASE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Recipe:
   def __init__(self, data:dict):
      self.id = data['id']
      self.name = data['name']
      self.description = data['description']
      self.instructions = data['instructions']
      self.time = data['time']
      self.under = data['under']
      self.user_id = data['user_id']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']

      #Add additional columns from database here

   def info(self):
      returnStr = f"First Name = {self.name} || Last Name = {self.description} || instructions = {self.instructions} time = {self.time}, under = {self.under}"
      return returnStr

#CREATE
   @classmethod
   def create_one(cls, data:dict):
      query = "INSERT INTO recipes (name, description, instructions, time, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(time)s, %(under)s, %(user_id)s)"
      print("this is the model file")
      result = connectToMySQL(DATABASE).query_db(query, data)
      print(data)
      return result
       
   # now we use the class methods to query our database 

#READ
   @classmethod
   def get_all(cls) -> list:
      query = "SELECT * FROM recipes;"
      #make sure to call the connectToMySQL function with the schema you are targeting

      results = connectToMySQL(DATABASE).query_db(query)
      #create an empty list to append our instances of recipes
      if not results:
         return []

      instance_list = []
      # iterate over the db results anad create instances of recipes with cls.
      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list

   @classmethod
   def get_one(cls, data):
      query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if not results:
         return []

      instance_list = []

      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list


   @classmethod
   def get_by_email(cls,data):
      query = "SELECT * FROM recipes WHERE email = %(email)s;"
      result = connectToMySQL(DATABASE).query_db(query,data)
      # Didn't find a matching user
      if len(result) < 1:
         return False
      return cls(result[0])


# Validators

   @staticmethod
   def validator(data: dict) -> bool:
      is_valid = True

      if(len(data['name']) < 2):
         flash("First Name must be more than 2 Characters in length", "err_recipes_name")
         is_valid = False

      if(len(data['description']) < 1):
         flash("Description must be more than 1 Characters in length", "err_recipes_description")
         is_valid = False

      if(len(data['instructions']) < 1):
         flash("Instructions must be more than 1 character in length", "err_recipes_instructions")
         is_valid = False


      if(len(data['time'])) ==0:
         flash("A date needs to be selected", "err_recipes_time")
         is_valid = False

      if 'under' not in data:
         flash("Did the recipe take longer than 30 minutes to make?", "err_recipes_under")
         is_valid = False


      return is_valid
      #run through some if checks -> if if checks come out to be bad then is_valid = False



# SAVE
   @classmethod
   def save(cls,data):
      query = "INSERT INTO recipes (name, description, email, password) VALUES (%(name)s, %(description)s, %(email)s, %(password)s);"
      result = connectToMySQL(DATABASE).query_db(query, data)
      return result

   #DELETE
   @classmethod
   def delete(cls, data):
      query = "DELETE FROM recipes WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

   #UPDATE
   @classmethod
   def update(cls, data):
      query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, time = %(time)s, under = %(under)s WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

# for the show route to show the one recipe that you selected on the "view recipe" URL
   @classmethod
   def get_one_recipe(cls, data):
      query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if results:

         one_recipe = cls(results[0])
         for dictionary in results:

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
            print(users_data)

            u = model_user.User(users_data)
            one_recipe.u = u
         return one_recipe

# for the display route where it shows the user that created the recipe in the "posted by" coloumn
   @classmethod
   def get_recipes(cls):
      query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
      print(query)
      results = connectToMySQL(DATABASE).query_db(query)
      if results:

         instance_list = []

         for dictionary in results:
            one_recipe = cls(dictionary)

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
            print(users_data)

            u = model_user.User(users_data)
            one_recipe.u = u
            instance_list.append(one_recipe)
         return instance_list
