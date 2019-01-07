"""
You will need a Postgres DB to run this. For development, you can run using Docker:
docker pull postgres
    docker run -p 5432:5432 --name data_coll_db \
        -e POSTGRES_PASSWORD=mypassword \
        -e POSTGRES_USER=user\
        -d postgres

If you want an easy way to interact with DB:
    docker pull dpage/pgadmin4
    docker run -p 80:80 \
        -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
        -e "PGADMIN_DEFAULT_PASSWORD=mypassword" \
        -d dpage/pgadmin4
"""
from flask import Flask, render_template, request
# Not sure why this is showing an error in vscode...
from flask_sqlalchemy import SQLAlchemy # You need to have installed both Flask-SQLAlchemy & psycopg2 with pip/pip3
from sqlalchemy.sql import func
from send_email import send_email

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:mypassword@postgresdb/height_collector'
db = SQLAlchemy(application)
db.create_all()
print("db.create_all() ran")

# Example: http://flask-sqlalchemy.pocoo.org/2.3/quickstart/#a-minimal-application
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)
    print("__tablename__ ran")

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_
        print("Data __init__ ran")

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/success", methods=['POST']) # by default, route only answers GET requests
def success():
    if request.method == 'POST':
        email = request.form['email_address']
        height = request.form['height']
        print(email, height)
        # print(request.form) # This will give you an ImmutableMultiDict with all form values
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            height_count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, height_count)
            return render_template("success.html")
        
    return render_template("index.html", text="Your data has already been collected!")

if __name__ == '__main__':
    application.run(debug=True)