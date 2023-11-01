from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument




@app.route("/recipe/new")
def new_recipe():
    if not "user_id" in session:
        return redirect('/')

        recipes = Recipe.get_all()
    recipes= Recipe.get_all()
    return render_template("new.html", recipes=recipes)

@app.route("/create_recipe", methods=['POST'])
def create_recipe():
    is_valid = Recipe.validator(request.form)
    if not is_valid:
        return redirect('/recipe/new')
    data = {
      'name': request.form['name'],
      'description': request.form['description'],
      'instructions': request.form['instructions'],
      'time': request.form['time'],
      'under': request.form['under'],
      'user_id': session['user_id']
    }
    id = Recipe.create_one(data)
    return redirect("/dashboard")

# Show Recipe

@app.route("/recipe/<int:id>")
def recipe_show_id(id):
    print("*********",id,"**********")
    if not "user_id" in session:
      return redirect('/')

    recip = Recipe.get_recipes()
    recipes = Recipe.get_one_recipe({ 'id': id})
    user = User.get_one({ 'id': session['user_id']})
    return render_template("Show_recipe.html", recipes = recipes, user = user, recip=recip )

# Delete Recipe
@app.route("/recipe/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
   data = {
      'id': recipe_id
   }
   Recipe.delete(data)
   return redirect("/dashboard")

# Edit Recipe

@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
  if not "user_id" in session:
    return redirect('/')

    is_valid = Recipe.validator(request.form)
    if not is_valid:
        return redirect('/recipe/edit')

  data = {"id" : id}
  recipes = Recipe.get_one_recipe(data)
  print(recipes)
  user = User.get_one({ 'id': session['user_id']})
  return render_template("Recipe_edit.html", recipes = recipes, user=user)


@app.route("/recipe/edit", methods=['POST'])
def update_recipe():
    print("\n\n\n\n\n******************************", request.form)
    is_valid = Recipe.validator(request.form)
    if not is_valid:
        return redirect(f"/recipe/edit/{request.form['id']}")
    data = {
      'id' : request.form['id'],
      'name': request.form['name'],
      'description': request.form['description'],
      'instructions': request.form['instructions'],
      'time': request.form['time'],
      'under': request.form['under'],
      'user_id': session['user_id']
    }
    Recipe.update(data)
    return redirect("/dashboard")

