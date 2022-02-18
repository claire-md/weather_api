from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os, requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + API_KEY

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    units = request.form["units"]
    city = request.form.get("city")
    # If not a vaild name for a city flashes an error message
    if len(city) < 2 or city.isdigit():
        flash("Please enter a valid city", category="error")
        return redirect(url_for("home"))

    complete_url = base_url + "&q=" + city + "&units=" + units
    response = requests.get(complete_url)
    res_json = response.json()
    if res_json["cod"] != 200:  # If not a valid city flashes an error messages
        flash("Please enter a valid city", category="error")
        return redirect(url_for("home"))

    # Storing all the needed data from OpenWeather
    country = res_json["sys"]["country"]
    temp = res_json["main"]["temp"]
    feel_temp = res_json["main"]["feels_like"]
    humidity = res_json["main"]["humidity"]
    description = res_json["weather"][0]["description"]
    icon = res_json["weather"][0]["icon"]

    return render_template("temperature.html",
                           city=city.title(),
                           unit=units,
                           country=country,
                           temp=temp,
                           feel_temp=feel_temp,
                           humidity=humidity,
                           description=description.title(),
                           icon=icon)


if __name__ == "__main__":
    app.run(debug=True)