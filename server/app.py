# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    # Query the database for the earthquake by ID
    earthquake = Earthquake.query.get(id)
    
    # If earthquake is found, return the attributes in JSON format
    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    # If earthquake is not found, return a 404 error with a message
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with a magnitude greater than or equal to the specified value
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Format the result as a list of dictionaries
    quakes_data = [quake.to_dict() for quake in quakes]
    
    # Return a JSON response with the count and list of earthquakes
    return jsonify({
        "count": len(quakes),
        "quakes": quakes_data
    }), 200


if __name__ == '__main__':
    app.run(port=5555)