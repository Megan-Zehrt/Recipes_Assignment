from flask_app import app
from flask_app.controllers import controller_user, controller_recipe
app.secret_key = 'the secret key, key the secret of the secret key I think?'


#end of the moving content
if __name__ == "__main__":
    app.run(debug=True)