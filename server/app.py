# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask import jsonify

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
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    
    if not earthquake:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
    return jsonify({
        "id": earthquake.id,
        "magnitude": earthquake.magnitude,
        "location": earthquake.location,
        "year": earthquake.year
    }), 200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    
    # Query all earthquakes with magnitude >= given value
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Build response
    response = {
        "count": len(quakes),
        "quakes": [
            {
                "id": q.id,
                "location": q.location,
                "magnitude": q.magnitude,
                "year": q.year
            }
            for q in quakes
        ]
    }
    
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
