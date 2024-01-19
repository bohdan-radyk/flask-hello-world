import requests

apiKey = "xTchVjRd25wPiXU2yEfvMBcya7LtdXO8"
myLocation = "Maribor"
baseUrl = "https://www.mapquestapi.com/geocoding/v1/address";

url = baseUrl + "?" + \
      "location="+myLocation+\
      "&key="+apiKey;
response = requests.get(url)
json_reps = response.json();
lat = json_reps["results"][0]["locations"][0]["latLng"]["lat"];
lng = json_reps["results"][0]["locations"][0]["latLng"]["lng"];
print("The cordinates of " + myLocation + " are: " + str(lat) + "," + str(lng))


tunings = {
    "Tuning1": {
        "E": 267,
        "A": 101
    },
    "Tuning2": {
        "E": 267,
        "A": 101
    }
}

