from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from marshmallow import post_load, fields, ValidationError
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
    price = db.Column(db.Float)
    inventory_quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.name} {self.description} {self.price} {self.inventory_quantity}"

# Schemas
class JeansSchema(ma.Schema):
    id = fields.Integer(primary_key = True)
    name = fields.String(required = True)
    description = fields.String(required = True)
    price = fields.Float()
    inventory_quantity = fields.Integer()

    class Meta:
        fields = ("id", "name", "description", "price", "inventory_quantity")

    @post_load
    def create_jean(self, data, **kwargs):
        return Jeans(**data)

jean_schema = JeansSchema()
jeans_schema = JeansSchema(many = True)


# Resources
class JeansListResource(Resource):
    def get(self):
        all_jeans = Jeans.query.all()
        return jeans_schema.dump(all_jeans)
    
    def post(self):
        form_data = request.get_json()
        try:
            new_jean = jean_schema.load(form_data)
            db.session.add(new_jean)
            db.session.commit()
            return jean_schema.dump(new_jean), 201
        except ValidationError as err:
            return err.messages, 400
    
class JeanResource(Resource):
    def get(self, jean_id):
        jean_from_db = Jeans.query.get_or_404(jean_id)
        return jean_schema.dump(jean_from_db), 200
    
    def delete(self, jean_id):
        jean_from_db = Jeans.query.get_or_404(jean_id)
        db.session.delete(jean_from_db)
        return "", 204
    
    def put(self, jean_id):
        jean_from_db = Jeans.query.get_or_404(jean_id)
        if "name" in request.json:
            jean_from_db.name = request.json["name"]
        if "description" in request.json:
            jean_from_db.description = request.json["description"]
        if "price" in request.json:
            jean_from_db.price = request.json["price"]
        if "inventory_quantity" in request.json:
            jean_from_db.inventory_quantity = request.json["inventory_quantity"]
        db.session.commit()
        return jean_schema.dump(jean_from_db), 200


# Routes
api.add_resource(JeansListResource, "/api/jeans")
api.add_resource(JeanResource, "/api/jeans/<int:jean_id>")