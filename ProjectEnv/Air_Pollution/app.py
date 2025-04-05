from flask import Flask, render_template, jsonify
import pandas as pd
import folium

app = Flask(__name__, template_folder="templates", static_folder="static")

# Fetch data from CSV
def get_pollution_data():
    df = pd.read_csv("data.csv")
    pollution_data = []

    for _, row in df.iterrows():
        pollution_data.append({
            "name": row["location"],
            "latitude": row["lat"],
            "longitude": row["lng"],
            "pm25": row["pm25"]
        })
    
    return pollution_data

# Generate folium map
def generate_map():
    data = get_pollution_data()
    m = folium.Map(location=[30.765, 76.786], zoom_start=17)

    for place in data:
        folium.Marker(
            location=[place["latitude"], place["longitude"]],
            popup=f"{place['name']}<br>PM2.5: {place['pm25']}",
            icon=folium.Icon(color="red" if place["pm25"] > 50 else "green")
        ).add_to(m)

    m.save("static/map.html")

@app.route("/")
def index():    
    generate_map()
    return render_template("index.html")

@app.route("/get_data")
def get_data():
    return jsonify(get_pollution_data())

if __name__ == "__main__":
    app.run(debug=True)
