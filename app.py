from flask import Flask, render_template, redirect, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
def jsonify_locations(locations):
    result = []
    for location in locations:
        result.append({
            "id": location.id,
            "name": location.name,
            "description": location.description
        })
    return result

@app.route('/locations')
def get_location():
    locations = Location.query.all();
    return jsonify_locations(locations);

@app.route('/delete')
def delete():
    id = request.args["id"]
    Location.query.filter(Location.id == id).delete();
    db.session.commit();
    return jsonify_locations(Location.query.all())
@app.route("/add-location")
def add_location():
    location = Location()
    location.name = request.args["name"]
    location.description = request.args["description"]
    db.session.add(location)
    db.session.commit();
    return jsonify_locations([location]);

@app.route("/get-location")
def get_location_by_id():
    id = request.args["id"]
    location = Location.query.get(id)
    return jsonify_locations([location]);


if __name__ == "__main__":
    print("Start connecting to DB")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'URL to DB here'
    db.init_app(app);
    with app.app_context():
        db.create_all();
        print("Connected")
        print("Adding dummy locatioon")
        location1 = Location()
        location1.name = "Test Location 1"
        location1.description = "Description 1"
        db.session.add(location1)
        db.session.commit()

    app.run();
