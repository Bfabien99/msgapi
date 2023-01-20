from flask import Flask
from blueprints.main import main
from blueprints.auth import auth
from blueprints.users import users

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(users)

if(__name__) == '__main__':
    app.run()