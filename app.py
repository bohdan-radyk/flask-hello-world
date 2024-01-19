from flask import Flask, render_template, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

locations = [
    {
        "id": 1,
        "name": "Lviv",
        "desc": "My home town"
    },
    {
        "id": 2,
        "name": "Maribor",
        "desc": "I'd love to visit!"
    }
]

id = 2;

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/locations')
def get_location():
    return locations;

@app.route('/delete/<id>')
def delete(id):
    for location in locations:
        if location["id"] == int(id):
            locations.remove(location);
    return redirect("/");

@app.route("/add-location")
def add_location():
    return render_template("add-location.html");

@app.route("/submit-location")
def submit_location():
    global id
    global locations
    id = id + 1;
    newLocation = {
        "id": id,
        "name": request.args["name"],
        "desc": request.args["description"]
    };
    locations.append(newLocation);
    return locations;


if __name__ == "__main__":
    app.run();
