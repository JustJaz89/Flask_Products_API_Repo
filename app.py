from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Jeans(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Integer)
    inventory_quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.name} {self.description} {self.price} {self.inventory_quantity}"

# Schemas
class JeansSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "inventory_quantity")

jean_schema = JeansSchema()
jeans_schema = JeansSchema(many = True)


# Resources
class JeansListResource(Resource):
    def get(self):
        all_jeans = Jeans.query.all()
        return jeans_schema.dump(all_jeans)
    
    def post(self):
        print(request)
        new_jean = Jeans(
            name = request.json["name"],
            description = request.json["description"],
            price = request.json["price"],
            inventory_quantity = request.json["inventory_quantity"]
        )
        db.session.add(new_jean)
        db.session.commit()
        return jean_schema.dump(new_jean), 201


# Routes
api.add_resource(JeansListResource, "/api/jeans")