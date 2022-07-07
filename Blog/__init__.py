
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "@3$5secret_Key&%@12374#@$%*"

# setup mysql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/blogsite'
# for heroku postgresql deployment
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gpidxehvatdriz:ca83ef381129816b88de720b84689e7e1605b42e54bba6a810506b6f06dc5080@ec2-3-222-74-92.compute-1.amazonaws.com:5432/d9phavipm0gbcm'
    # 'postgresql://vntxvszostkgmi:fc777eadb31a89ad64023bc7ee723f6541127ff512f9695148ae84aa6613cd1a@ec2-34-233-115-14.compute-1.amazonaws.com:5432/dfumsja3m0dnjo'
db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()


# For migration
migrate = Migrate(app, db)
# with app.app_context():
#     if db.engine.url.drivername == "mysql":
#         migrate.init_app(app, db, render_as_batch=True)
#     else:
#         migrate.init_app(app, db)

# for login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



from Blog.blogs import routes
from Blog.users import routes
from Blog.admin import routes


